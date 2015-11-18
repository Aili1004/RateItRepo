import datetime
import logging
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext.ndb import blobstore


class Agency(ndb.Model):
    GTFS_FILE_NAME = 'agency.txt'
    GTFS_KEY_PROPS = ['agency_id']
    agency_id = ndb.StringProperty(required=True)
    agency_name = ndb.StringProperty(required=True)
    agency_url = ndb.StringProperty(required=True)
    agency_timezone = ndb.StringProperty(required=True)
    agency_lang = ndb.StringProperty(required=True)
    agency_phone = ndb.StringProperty(required=True)


class CalendarDates(ndb.Model):
    GTFS_FILE_NAME = 'calendar_dates.txt'
    GTFS_KEY_PROPS = ['service_id', 'date', 'exception_type']
    service_id = ndb.StringProperty(required=True)
    date = ndb.StringProperty(required=True)
    exception_type = ndb.StringProperty(required=True)


class Calendar(ndb.Model):
    GTFS_FILE_NAME = 'calendar.txt'
    GTFS_KEY_PROPS = ['service_id', 'start_date']
    service_id = ndb.StringProperty(required=True)
    monday = ndb.IntegerProperty(required=True)
    tuesday = ndb.IntegerProperty(required=True)
    wednesday = ndb.IntegerProperty(required=True)
    thursday = ndb.IntegerProperty(required=True)
    friday = ndb.IntegerProperty(required=True)
    saturday = ndb.IntegerProperty(required=True)
    sunday = ndb.IntegerProperty(required=True)
    start_date = ndb.DateProperty(required=True)
    end_date = ndb.DateProperty(required=True)


class Routes(ndb.Model):
    GTFS_FILE_NAME = 'routes.txt'
    GTFS_KEY_PROPS = ['route_id']
    route_id = ndb.StringProperty(required=True)
    agency_id = ndb.StringProperty(required=True)
    route_short_name = ndb.StringProperty(required=True)
    route_long_name = ndb.StringProperty(required=True)
    route_desc = ndb.StringProperty(required=True)
    route_type = ndb.StringProperty(required=True)
    route_color = ndb.StringProperty(required=True)
    route_text_color = ndb.StringProperty(required=True)


class Shapes(ndb.Model):
    GTFS_FILE_NAME = 'shapes.txt'
    GTFS_KEY_PROPS = ['shape_id', 'shape_pt_sequence']
    shape_id = ndb.StringProperty(required=True)
    shape_pt_lat = ndb.FloatProperty(required=True)
    shape_pt_lon = ndb.FloatProperty(required=True)
    shape_pt_sequence = ndb.IntegerProperty(required=True)
    shape_dist_traveled = ndb.FloatProperty(required=True)


class StopTimes(ndb.Model):
    GTFS_FILE_NAME = 'stop_times.txt'
    GTFS_KEY_PROPS = ['stop_id', 'stop_sequence']
    trip_id = ndb.StringProperty(required=True)
    arrival_time = ndb.IntegerProperty(required=True)
    departure_time = ndb.IntegerProperty(required=True)
    stop_id = ndb.StringProperty(required=True)
    stop_sequence = ndb.IntegerProperty(required=True)
    stop_headsign = ndb.StringProperty(required=True)
    pickup_type = ndb.StringProperty(required=True)
    drop_off_type = ndb.StringProperty(required=True)
    shape_dist_traveled = ndb.FloatProperty(required=True)


class Stops(ndb.Model):
    GTFS_FILE_NAME = 'stops.txt'
    GTFS_KEY_PROPS = ['stop_id']
    stop_id = ndb.StringProperty(required=True)
    stop_code = ndb.StringProperty(required=True)
    stop_name = ndb.StringProperty(required=True)
    stop_lat = ndb.FloatProperty(required=True)
    stop_lon = ndb.FloatProperty(required=True)
    location_type = ndb.StringProperty(required=True)
    parent_station = ndb.StringProperty(required=True)
    wheelchair_boarding = ndb.StringProperty(required=True)
    platform_code = ndb.StringProperty(required=True)
    
    @classmethod
    def find(cls):
        parent = Uploads.get_active_key()
        return ndb.gql("SELECT * FROM Stops WHERE ANCESTOR IS :1", parent)


class Trips(ndb.Model):
    GTFS_FILE_NAME = 'trips.txt'
    GTFS_KEY_PROPS = ['trip_id']
    route_id = ndb.StringProperty(required=True)
    service_id = ndb.StringProperty(required=True)
    trip_id = ndb.StringProperty(required=True)
    shape_id = ndb.StringProperty(required=True)
    trip_headsign = ndb.StringProperty(required=True)
    direction_id = ndb.IntegerProperty(required=True)
    block_id = ndb.StringProperty(required=True)
    wheelchair_accessible = ndb.IntegerProperty(required=True)


class TripsStops(ndb.Model):
    GTFS_FILE_NAME = 'trips_stops.txt'
    GTFS_KEY_PROPS = ['route_id', 'stop_id']
    route_id = ndb.StringProperty(required=True)
    stop_id = ndb.StringProperty(required=True)


class TripsHeadsigns(ndb.Model):
    GTFS_FILE_NAME = 'trips_headsigns.txt'
    GTFS_KEY_PROPS = ['route_id', 'direction_id', 'trip_headsign', 'trip_headsign_return']
    route_short_name = ndb.StringProperty(required=True)
    route_id = ndb.StringProperty(required=True)
    direction_id = ndb.IntegerProperty(required=True)
    trip_headsign = ndb.StringProperty(required=True)
    trip_headsign_return = ndb.StringProperty(required=True)

    @classmethod
    def find(cls):
        parent = Uploads.get_active_key()
        return ndb.gql("SELECT * FROM TripsHeadsigns WHERE ANCESTOR IS :1", parent)


# List of all GTFS model classes.
#GTFS_MODELS=(Agency, Routes, Stops, Trips, StopTimes, CalendarDates, Calendar, Shapes, TripsStops, TripsHeadsigns)

# Abbreviated list bec
GTFS_MODELS=(Agency, Routes, Stops, Trips, TripsStops, TripsHeadsigns)

class Uploads(ndb.Model):
    file_key = blobstore.BlobKeyProperty(required=True)
    is_processed = ndb.BooleanProperty(required=True)
    is_processing = ndb.BooleanProperty(required=True)
    processing_attempts = ndb.IntegerProperty(required=False)
    processed_status = ndb.StringProperty(required=False)
    time_loaded = ndb.DateTimeProperty(required=True, auto_now=True)
    time_processing_started = ndb.DateTimeProperty(required=False)
    time_processing_ended = ndb.DateTimeProperty(required=False)
    
    MOST_RECENT_GTFS_UPLOAD_KEY = 'MOST_RECENT_GTFS_UPLOAD_KEY'
    
    @classmethod
    def _pre_delete_hook(cls, key):
        # Delete blobstore file on deletion on Upload.
        # This is unreliable as it won't get triggered if deleted from
        # the admin console.
        entity = key.get()
        # Make sure we have an entity.
        if not entity:
            return
        blobstore.delete(entity.file_key)
        
    @classmethod
    def get_active_key(cls):
        # Returns the most active key.
        key = memcache.get(Uploads.MOST_RECENT_GTFS_UPLOAD_KEY)
        if key:
            return key
        upload = Uploads.find_most_recent_active_gtfs_upload()
        if upload:
            key = upload.key
            memcache.add(Uploads.MOST_RECENT_GTFS_UPLOAD_KEY, key, 600)
            return key
        logging.error(
            "GTFS data is not available, you will need to upload a filtered gtfs file "
            "to populate the GTFS data.  A file is available here: "
            "https://bitbucket.org/ahau3752/rateitrepo/downloads/filtered_gtfs_static_2014-10-15-a.zip")

        return None

    @classmethod
    def find_most_recent_active_gtfs_upload(cls):
        return ndb.gql(
            "SELECT * FROM Uploads where is_processed = True order by time_loaded desc limit 1").get()
        
