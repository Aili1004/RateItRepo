import webapp2
import csv
import os
import jinja2
import logging
import datetime
import zipfile
from google.appengine.ext.ndb import blobstore
from urlparse import urlparse
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import deferred
from google.appengine.ext import ndb

import models.gtfs


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class operator_upload_gtfs(blobstore_handlers.BlobstoreUploadHandler, webapp2.RequestHandler):
    def get(self):
	
        page_title = "Upload GTFS"
        
        parsed = urlparse(self.request.url)
        upload_url = blobstore.create_upload_url(parsed.path)

        template_values = {
            'page_title': page_title,
            'upload_url' : upload_url,
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/operator_upload_gtfs.html')
        self.response.write(template.render(template_values))
        
        
    # Handles uploaded blobs.
    def post(self):
        uploads = self.get_uploads('gtfs_file')
        unused_uploads = self.get_uploads()
        try:
            for upload in uploads:
                record = models.gtfs.Uploads(
                    file_key=upload.key(),
                    is_processed=False,
                    is_processing=False,
                    processing_attempts=0
                    )
                record.put()
                # Run the processing in a background request (using task queue)
                deferred.defer(process_gtfs_file, record.key)
                unused_uploads.remove(upload)
                
        finally:
            # Remove malicious uploads.
            keys = [upload.key() for upload in unused_uploads]
            blobstore.delete_multi(keys)
            
        self.redirect(urlparse(self.request.url).path + "?uploaded=t")
        
 
# Process the gtfs file.
# Running this in a task queue task means we have 10 minutes to process the task.
def process_gtfs_file(key):
    logging.info("process_gtfs_file %r" % key)
    
    success = False
    
    try:
        (locked, entity) = processing_lock(key)
        # Attempt to take the lock on the key (by marking the Upload record as processing).
        if not locked:
            success = True  # Some other task is currently processing.
            return
            
        success = process_gtfs_file_has_lock(entity)
        if not success:
            raise Exception  # Forces retry of task.
        
        # Unlock and complete processing
        entity.is_processed = True
        entity.is_processing = False
        entity.processed_status = "Success"
        entity.time_processing_ended = datetime.datetime.now()
        entity.put()
        
        return

    finally:
        if not success:
            processing_unlock(key)


# The record is now locked so we can read the blob and process the gtfs file.
def process_gtfs_file_has_lock(entity):

    reader = blobstore.BlobReader(entity.file_key)
    zip = zipfile.ZipFile(reader, 'r')
    
    for model in models.gtfs.GTFS_MODELS:
      logging.info("started processing %s" % model.GTFS_FILE_NAME)
      process_gtfs_csv(entity.key, zip, model)
      logging.info("ended processing %s" % model.GTFS_FILE_NAME)

    return True
    
def _pass(v):
    return v
    
def _date(v):
    return datetime.datetime.strptime(v, "%d%m%Y").date()
    
def _time(v):
    return datetime.datetime.strptime(v, "%H:%M:%S").time()

# The times in stop_times.txt are larger than 24hrs since they cater for stops after midnight.
def _overtime(v):
    hs, ms, ss = v.split(':')
    return int(hs) * 3600 + int(ms) * 60 + int(ss)

CONVERSION_FUNCTION_BY_PROPERTY = {
    'arrival_time' : _overtime,
    'departure_time' : _overtime,
}

CONVERSION_FUNCTION = {
    ndb.StringProperty: _pass,
    ndb.BooleanProperty: bool,
    ndb.DateProperty: _date,
    ndb.TimeProperty: _time,
    ndb.IntegerProperty: int,
    ndb.FloatProperty: float,
}

MAX_WRITE_SIZE = 100

def make_key(model, parent, record):
    keyname = ':'.join([record[prop] for prop in model.GTFS_KEY_PROPS])
    return ndb.Key(model, keyname, parent=parent)
    

def process_gtfs_csv(parent, zip, model):
    filename = model.GTFS_FILE_NAME
    csvfile = csv.DictReader(zip.open(filename))
    
    entities = []
    previous_futures = []
    try:
        for record in csvfile:
            converted_rec = {}
            for name, value in record.items():
               dest_type = type(getattr(model, name))
               try:
                   func = CONVERSION_FUNCTION_BY_PROPERTY.get(name, CONVERSION_FUNCTION[dest_type])
                   converted_rec[name] = func(value)
               except:
                   logging.log(logging.ERROR, "failed to convert '%s' to a %s" % (value, dest_type))
                   raise
            converted_rec['key'] = make_key(model, parent, record)
            entities.append(model(**converted_rec))
            
            if len(entities) >= MAX_WRITE_SIZE:
                write_entities(previous_futures, entities)
    finally:
        write_entities(previous_futures, entities)
        write_entities(previous_futures, entities)


@ndb.transactional
def write_entities(previous_futures, entities):
    next_futures = ndb.put_multi_async(entities)
    entities[:] = []
    prev_entities = [future.get_result() for future in previous_futures]
    previous_futures[:] = next_futures

@ndb.transactional
def processing_lock(key):
    entity = key.get()
    
    # Removal of the Upload record means it's done for.
    if not entity:
        return (False, entity)
    
    # If we're already processing or in process then move on.
    if entity.is_processing or entity.is_processed:
        return (False, entity)
    
    entity.is_processing = True
    entity.time_processing_started = datetime.datetime.now()
    entity.processing_attempts += 1
 
    entity.put()
    
    return (True, entity)
    

@ndb.transactional
def processing_unlock(key):
    entity = key.get()

    entity.is_processing = False
 
    entity.put_async()

    
