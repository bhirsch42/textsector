import webapp2
import cgi
import os
import jinja2
import logging
import hashlib
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

cookie_secret = "fight_club"

class User(ndb.Model):
	username = ndb.StringProperty()
	password = ndb.StringProperty()

class Handler(webapp2.RequestHandler):

 	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		self.user_cookie_name = 'user_id'
		uid = self.read_secure_cookie(self.user_cookie_name)
		self.user = uid and User.get_by_id(int(uid))

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def getDefaultHeader(self):
		template = jinja_env.get_template('DefaultPageHeader.html')
		if self.user:
			return template.render(username=self.user.username)
		else:
			return template.render(username=None)


	def set_secure_cookie(self, name, val, days = None):
		cookie_val = make_secure_val(str(val))
		if days == None:
			self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))
		else:
			expiration = datetime.datetime.now() + datetime.timedelta(days = days)
			self.response.headers.add_header('Set-Cookie', '%s=%s; expires=%s; Path=/;' % (name, cookie_val, expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")))


	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		if cookie_val and check_secure_val(cookie_val):
			return cookie_val.split('|')[0]

	def render_default_header(self):
		self.write(self.getDefaultHeader())


def my_hash(val):
	return str(hashlib.sha256(val).hexdigest())

def make_secure_val(val):
	return "%s|%s" % (val, my_hash(val + cookie_secret))

def check_secure_val(secure_val):
	val = secure_val.split('|')[0]
	if secure_val == make_secure_val(val):
		return val

