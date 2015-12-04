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
    ignore = ndb.BooleanProperty(default=False)

class Randomstevilka(ndb.Model):
    stevilo = ndb.IntegerProperty()
    uganil = ndb.StringProperty()
    vposkusih = ndb.IntegerProperty()
    zadnjiposkus = ndb.IntegerProperty()
    zadnirezultat = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

class Obletnice(ndb.Model):
    event = ndb.StringProperty()
    datum = ndb.DateProperty()
    pripada = ndb.StringProperty()
    leto = ndb.IntegerProperty()
    mesec = ndb.IntegerProperty()
    dan = ndb.IntegerProperty()
    doroka = ndb.IntegerProperty(default=0)