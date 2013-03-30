import webapp2
import cgi
import os
import jinja2
import logging
import hashlib
from google.appengine.ext import ndb

cookie_secret = "fight_club"

def my_hash(val):
	return str(hashlib.sha256(val).hexdigest())

def make_secure_val(val):
	return "%s|%s" % (val, my_hash(val + cookie_secret))

def check_secure_val(secure_val):
	val = secure_val.split('|')[0]
	if secure_val == make_secure_val(val):
		return val

