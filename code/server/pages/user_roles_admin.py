import webapp2
import os
import jinja2
import logging
from operator_handler import ResearcherHandler
from models.user_roles import UserRoles
from google.appengine.api import users
import main

from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Mapping of form field names to datastore field names for roles.
FORM_DB_MAP = {
    'operator' : 'is_operator_role',
    'researcher' : 'is_researcher_role'}

class user_roles_admin(ResearcherHandler):
    def get(self):
        page_title = "User Roles Administration"
        entities = UserRoles.query()
		
        template_values = self.make_template_dict(
            page_title=page_title,
            entities=entities)

        template = JINJA_ENVIRONMENT.get_template('templates/user_roles_admin.html')
        self.response.write(template.render(template_values))		
		
    def post(self):
        if self.request.get('create_user_admin_submit') == "1":
            emailAddress = self.request.get('emailAddress')
            user_roles = ndb.Key(UserRoles, emailAddress).get()
            if not user_roles:
                user_roles = UserRoles(id=emailAddress)
            user_roles.is_operator_role = self.request.get('operator') == 'True'
            user_roles.is_researcher_role = self.request.get('researcher') == 'True'
            user_roles.put()

        elif self.request.get('submit_changes') == "1":
            self.fetched_recs = {}
            self.modified_recs = {}
            current_user_email = users.get_current_user().email()
            for arg in self.request.arguments():
                arg_split = arg.split(':')
                if len(arg_split) != 2:
                    continue
                (role_type, email) = arg_split
                if not FORM_DB_MAP.has_key(role_type):
                    logging.warning('Form field is unknown %s' % arg)
                    continue
                db_role = FORM_DB_MAP[role_type]
                rec = self.fetch(email)
                if not rec:
                    continue
                value = self.request.get(arg) == 'True'
                if current_user_email == email and role_type == 'researcher':
                    # Not allowed to modify the current user's researcher status.
                    logging.warning('Attempt to change the current user\'s admin role %s' % arg)
                    continue
                old_value = rec.to_dict()[db_role]
                if value != old_value:
                    rec.populate(**{db_role : value})
                    self.modified_recs[email] = rec
            # Records to be written now in modified_recs.
            ndb.put_multi(self.modified_recs.values())

        # Use a redirect so that page reloads don't cause submission to be rerun.
        self.redirect(self.request.path)
        
    def fetch(self, email):
        if self.fetched_recs.has_key(email):
            return self.fetched_recs.get(email)
        rec = UserRoles.get_by_email(email)
        self.fetched_recs[email] = rec
        return rec

    def get_submit_function_name(self):
        return 'user_roles_admin'