#!/usr/bin/env python
import os
import jinja2
import webapp2
from loggedin import is_logged_in
from google.appengine.api import urlfetch
from models import Sporocilo,Uporabniki
import json
import time



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
        return self.render_template("redirect.html" , params=params)

class CreateHandler(BaseHandler):
    def get(self):
        is_logged_in(params)
        seznamuserjev = Uporabniki.query().fetch()
        posiljatelj = {"prejemniki": seznamuserjev}
        params.update(posiljatelj)
        print "PARAMS"
        print params
        return self.render_template("create.html" , params=params)



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/create', CreateHandler),
    #webapp2.Route('/mymessages', MyMessagesHandler),
    #webapp2.Route('/sendmessages', SendMessagesHandler),
    webapp2.Route('/weather', WeatherHandler),
    webapp2.Route('/redirect', RedirectHandler),
], debug=True)
