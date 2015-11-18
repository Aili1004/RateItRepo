import logging
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import ndb


class UserRoles(ndb.Model):
    user_id = ndb.StringProperty()
    is_operator_role = ndb.BooleanProperty()
    is_researcher_role = ndb.BooleanProperty()
    
    @classmethod
    def is_operator(cls, user):
        user_rec = cls.get_by_email(user.email())
        if user_rec:
             return user_rec.is_operator_role
        return False
        
    @classmethod
    def is_researcher(cls, user):
        user_rec = cls.get_by_email(user.email())
        if user_rec:
             return user_rec.is_researcher_role
        return False

    @classmethod
    def create_admin_if_none_exists(cls, user):
        user_rec = cls.get_by_email(user.email())
        if user_rec:
             return
        user_rec = UserRoles(
            id=user.email(),
            user_id=user.user_id(),
            is_operator_role=True,
            is_researcher_role=True
            )
        user_rec.put()
        return
        
    @classmethod
    def get_by_email(cls, email):
        k = ndb.Key(UserRoles, email)
        return k.get()
