#!/usr/bin/env python
# coding=utf-8
import os
import json
import time

import jinja2
import webapp2
from lib.loggedin import is_logged_in
from google.appengine.api import urlfetch
from lib.models import Sporocilo,Uporabniki,Obletnice
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail
import datetime
from datetime import datetime

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)
params={}


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        is_logged_in(params)


        return self.render_template("index.html",params=params)

class WeatherHandler(BaseHandler):
    def get(self):
        #v urlju so parametri ki jih zelimo videti loceni z ikonco &
        # novo mesto 3194350 , 3239318 Ljubljana
        url = "http://api.openweathermap.org/data/2.5/group?id=3196359,3194351,2639110&units=metric&appid=29fb19f38dde3e3bfe9f2c2536b414b0"
        #zgornji je za vecmest, spodnji je za samo eno mesto
        #url = "http://api.openweathermap.org/data/2.5/weather?q=Ljubljana&units=metric&appid=29fb19f38dde3e3bfe9f2c2536b414b0"
        result = urlfetch.fetch(url)
        podatki = json.loads(result.content)
        params = {"podatki": podatki}
        is_logged_in(params)
        #print params
        self.render_template("weather.html", params=params)

class RedirectHandler(BaseHandler):
    def post(self):
        posiljat = self.request.get("posiljatelj")
        prejemni = self.request.get("prejemnik")
        sporocil = self.request.get("sporocilo")
        if sporocil != "Obvezno vpisi kaj notri":
            sporoc = Sporocilo(sender=posiljat, reciever=prejemni, message=sporocil)
            sporoc.put()
            time.sleep(1)
            mail.send_mail("podobnik.igor@gmail.com", prejemni, "novo sporocilo", "Nov mejl :) poglej na http://koncniprojekt.appspot.com/ Sporocilo pa je: %s" %sporocil)
        return self.render_template("redirect.html" , params=params)

class CreateHandler(BaseHandler):
    def get(self):
        is_logged_in(params)
        seznamuserjev = Uporabniki.query().fetch()
        posiljatelj = {"prejemniki":seznamuserjev}
        params.update(posiljatelj)
        #print "PARAMS"
        #print params
        return self.render_template("create.html" , params=params)


class MyMessagesHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        emailprejemnika = user.email()
        #fseznam = Forum.query().fetch()
        #v query das notri pogoj
        oldseznam = Sporocilo.query(ndb.AND(Sporocilo.reciever == emailprejemnika,Sporocilo.new == False)).fetch()
        newseznam = Sporocilo.query(ndb.AND(Sporocilo.reciever == emailprejemnika,Sporocilo.new == True)).fetch()
        # SORT order takole zgleda... reverse za najvecjega navzdol
        oldseznam = sorted(oldseznam, key=lambda dat:dat.created, reverse=True)
        params = {"seznam" : oldseznam, "new": newseznam }
        is_logged_in(params)
        #nova spremeni v stara

        for user in Sporocilo.query(ndb.AND(Sporocilo.reciever == emailprejemnika,Sporocilo.new == True)):
            user.new = False
            user.put()
        #ce bi zelel da vedno prvilno pokazemo stevilko pri novih sporocilih.
        #time.sleep(1)
        return self.render_template("prejeta.html" , params=params)


class SendMessagesHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        emailprejemnika = user.email()
        #fseznam = Forum.query().fetch()
        #v query das notri pogoj
        oldseznam = Sporocilo.query(ndb.AND(Sporocilo.sender == emailprejemnika,Sporocilo.new == False)).fetch()
        newseznam = Sporocilo.query(ndb.AND(Sporocilo.sender == emailprejemnika,Sporocilo.new == True)).fetch()
        # SORT order takole zgleda... reverse za najvecjega navzdol
        oldseznam = sorted(oldseznam, key=lambda dat:dat.created, reverse=True)
        newseznam = sorted(newseznam, key=lambda dat:dat.created, reverse=True)
        params = {"seznam" : oldseznam, "newseznam":newseznam }
        is_logged_in(params)
        return self.render_template("poslana.html" , params=params)

class TimeHandler(BaseHandler):
    def get(self):
        podatki = "DA"

        user = users.get_current_user()
        emailprejemnika = user.email()
        oldseznam = Obletnice.query(Obletnice.pripada == emailprejemnika).fetch()
        params = {"podatki": oldseznam}
        is_logged_in(params)

        self.render_template("times.html", params=params)



# preko redirecta reseno postanje datumov v tabelo.
class RedirecttimeHandler(BaseHandler):
    def post(self):
        user = users.get_current_user()
        emailprejemnika = user.email()
        rawdt = self.request.get("datum")
        leto = int(rawdt[:4])
        mesec = int(rawdt [5:7])
        dan = int(rawdt [8:10])

        #mogoce bi bilo bolje ce bi class naredil in te podatke notri dal - se boljse v bazo pisal locene podatke. sestavil nazaj ce treba. izracun naredil glede na podatke iz baze
        datum = datetime(leto,mesec,dan)
        dogodek = self.request.get("dogodek")
        if dogodek != "Obvezno vpisi kaj notri":
            dog = Obletnice(event=dogodek, datum=datum, pripada=emailprejemnika)
            dog.put()
            time.sleep(1)
        is_logged_in(params)
        return self.render_template("redirecttime.html" , params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/create', CreateHandler),
    webapp2.Route('/mymessages', MyMessagesHandler),
    webapp2.Route('/sendmessages', SendMessagesHandler),
    webapp2.Route('/weather', WeatherHandler),
    webapp2.Route('/redirect', RedirectHandler),
    webapp2.Route('/time', TimeHandler),
    webapp2.Route('/redirecttime', RedirecttimeHandler),
], debug=True)
