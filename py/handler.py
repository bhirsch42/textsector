import webapp2
import cgi
import os
import jinja2
import logging
import hashlib
from google.appengine.ext import ndb
from utils import *

class Handler(webapp2.RequestHandler):

	# set up jinja workspace
	template_dir = os.path.join(os.path.dirname(__file__), '../html')
	jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

	# calls default initializer (syntax for future, does nothing yet)
 	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	# returns html from jinja template with parameters as a string
	# takes template file name as first argument
	def render_str(self, template, **params):
		t = jinja_env.get_template(template_dir+template)
		return t.render(params)

	# writes to webpage from jinja template
	# takes template file name as first argument
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	# add a hashed cookie to the user's browser
	def set_secure_cookie(self, name, val, days = None):
		cookie_val = make_secure_val(str(val))
		if days == None:
			self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))
		else:
			expiration = datetime.datetime.now() + datetime.timedelta(days = days)
			self.response.headers.add_header('Set-Cookie', '%s=%s; expires=%s; Path=/;' % (name, cookie_val, expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")))

	# returns value from user's browser cookie, or None if cookie is invalid
	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		if cookie_val and check_secure_val(cookie_val):
			return cookie_val.split('|')[0]
