__author__ = 'igorpodobnik'
import datetime


from google.appengine.ext import ndb


class Sporocilo(ndb.Model):
    sender = ndb.StringProperty()
    reciever = ndb.StringProperty()
    message = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    new = ndb.BooleanProperty(default=True)

class Uporabniki(ndb.Model):
    user = ndb.StringProperty()
    approved = ndb.BooleanProperty(default=False)