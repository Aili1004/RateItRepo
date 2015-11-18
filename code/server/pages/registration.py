import webapp2
import os
import jinja2
import csv
from datetime import date, datetime
from google.appengine.api import users
from array import array
from urlparse import urlparse
from google.appengine.ext import ndb
from models.rateit_users import RateItUser
import main

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class registration(webapp2.RequestHandler):
    def get(self):
        self.setup_jinja()
        self.response.out.write(main.logging_link())
        self.response.out.write(main.get_pre_page())
    #     print out registered user info
        find_user = RateItUser.query(RateItUser.user==users.get_current_user())
        for item in find_user:
            self.response.out.write(item.user.email())
            self.response.out.write(item.user_type)
            self.response.out.write(item.user_sex)
            self.response.out.write(item.user_born_year)
            self.response.out.write(item.user_household_type)
            self.response.out.write(item.user_postcode)
            self.response.out.write(item.user_education)
            self.response.out.write(item.user_occupation)
            self.response.out.write(item.user_monthly_income)
            self.response.out.write(item.user_mobility_impairment)
            self.response.out.write(item.user_device)
            self.response.out.write(item.user_driver_licence)
            self.response.out.write(item.user_often_use)
            self.response.out.write(item.user_purpose_use)
            self.response.out.write(item.time_registered)

    def postcode_list(self):
        a = []
        csv_file = open('aus_postcodes.csv', 'rU')
        data = csv.reader(csv_file)
        next(data, None)
        for row in data:
            a.append(row[0]+", "+row[1])
        csv_file.close()
        return a

    def setup_jinja(self):
        page_title = "Registration"
        year_list = array('i', range(1900, date.today().year))

        template_values = {
            'page_title': page_title,
            'user_id': main.current_user().email(),
            'is_registered': main.is_registered(),
            'year_list': year_list,
            'postcode_list': self.postcode_list(),
        }

        template = JINJA_ENVIRONMENT.get_template('templates/registration.html')
        self.response.write(template.render(template_values))

    def post(self):
        new_user = RateItUser()
        new_user.user = main.current_user()
        new_user.user_type = "passenger"
        new_user.user_sex = self.request.get('sex').lower()
        new_user.user_born_year = self.request.get('inputYear')
        new_user.user_household_type = self.request.get('householdType')
        new_user.user_postcode = self.request.get('postcode')
        new_user.user_education = self.request.get('education')
        new_user.user_occupation = self.request.get('occupation')
        new_user.user_monthly_income = self.request.get('monthly_income')
        new_user.user_mobility_impairment = self.request.get('mobility_impairment')
        new_user.user_often_use = self.request.get('often_to_use')
        new_user.user_device = self.request.get('devices_type')
        new_user.user_driver_licence = self.request.get('drivers_licence')
        new_user.user_purpose_use = self.request.get('purpose_to_use')
        new_user.time_registered = datetime.today()


        if not main.is_registered():
            new_user.put()

        self.setup_jinja()
        self.redirect(main.get_pre_page())