import logging
import webapp2

from google.appengine.api import users
import models.user_roles


class OperatorHandler(webapp2.RequestHandler):
    """OperatorHandler handles all operator requests.
    """

    def user_interface_name(self):
        return 'operator'

    def get_template(self):
        return 'templates/operator_template.html'
        
    def init_admin(self):
        user = users.get_current_user()
        if users.is_current_user_admin():
            models.user_roles.UserRoles.create_admin_if_none_exists(user)

    def validate_user(self):
        self.init_admin()
        return models.user_roles.UserRoles.is_operator(users.get_current_user())

    def dispatch(self):
        if not self.validate_user():
            user = users.get_current_user()
            username = 'unknown'
            if user:
                username = user.nickname()
            logging.warning(
                'User %s attempted to log into %s interface at %s' %
                (
                    username,
                    self.user_interface_name(),
                    self.request.path,
                ))
            # Always redirect to the home page if the user is not an operator.
            self.redirect('/')
            return
        return super(OperatorHandler, self).dispatch()
    
    # Returns a dict with values specific to this handler.
    def make_template_dict(self, **kwds):
        kwds['extends_template'] = self.get_template()
        kwds['submit_path'] = self.get_submit_path()
        return kwds
        
    def get_submit_path(self):
        return '/' + self.user_interface_name() + '/' + self.get_submit_function_name()
        
    def get_submit_function_name(self):
        return ''


class ResearcherOverrides:
    """Overrides of OperatorHandler to provide researcher handler.
    """

    def user_interface_name(self):
        return 'researcher'

    def get_template(self):
        return 'templates/researcher_template.html'
        
    def validate_user(self):
        self.init_admin()
        return models.user_roles.UserRoles.is_researcher(users.get_current_user())

       
class ResearcherHandler(ResearcherOverrides, OperatorHandler):
    """Base class for researcher handlers.
    """
    pass
 
 