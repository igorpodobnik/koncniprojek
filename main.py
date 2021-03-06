#!/usr/bin/env python
# coding=utf-8
import os
import json
import time

import jinja2
import webapp2
from lib.loggedin import is_logged_in,preverividivse
from google.appengine.api import urlfetch
from lib.models import Sporocilo,Uporabniki,Obletnice,Randomstevilka
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail
import datetime
from datetime import datetime
from lib.obletnica import izracun,vnosdatuma
from lib.ugani import Random,generiraj_random




template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)
params={}
glavna_stevilka=3691

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
        vidi=preverividivse()
        if vidi == "da":
            seznamuserjev = Uporabniki.query().fetch()
            posiljatelj = {"prejemniki":seznamuserjev}
            params.update(posiljatelj)
        else:
            seznamuserjev = Uporabniki.query(Uporabniki.user == "podobnik.igor@gmail.com").fetch()
            posiljatelj = {"prejemniki":seznamuserjev}
            params.update(posiljatelj)

        #print "PARAMS"
        #print params
        return self.render_template("create.html" , params=params)


class MyMessagesHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            emailprejemnika = user.email()
        #fseznam = Forum.query().fetch()
        #v query das notri pogoj
            oldseznam = Sporocilo.query(ndb.AND(Sporocilo.reciever == emailprejemnika,Sporocilo.new == False)).fetch()
            newseznam = Sporocilo.query(ndb.AND(Sporocilo.reciever == emailprejemnika,Sporocilo.new == True)).fetch()
        # SORT order takole zgleda... reverse za najvecjega navzdol
            oldseznam = sorted(oldseznam, key=lambda dat:dat.created, reverse=True)
            params = {"seznam" : oldseznam, "new": newseznam }
        else:
            params ={}
        is_logged_in(params)
        #nova spremeni v stara
        if user:
            for user in Sporocilo.query(ndb.AND(Sporocilo.reciever == emailprejemnika,Sporocilo.new == True)):
                user.new = False
                user.put()
            #ce bi zelel da vedno prvilno pokazemo stevilko pri novih sporocilih.
        #time.sleep(1)
        return self.render_template("prejeta.html" , params=params)


class SendMessagesHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            emailprejemnika = user.email()
        #fseznam = Forum.query().fetch()
        #v query das notri pogoj
            oldseznam = Sporocilo.query(ndb.AND(Sporocilo.sender == emailprejemnika,Sporocilo.new == False)).fetch()
            newseznam = Sporocilo.query(ndb.AND(Sporocilo.sender == emailprejemnika,Sporocilo.new == True)).fetch()
        # SORT order takole zgleda... reverse za najvecjega navzdol
            oldseznam = sorted(oldseznam, key=lambda dat:dat.created, reverse=True)
            newseznam = sorted(newseznam, key=lambda dat:dat.created, reverse=True)
            params = {"seznam" : oldseznam, "newseznam":newseznam }
        else:
            params ={}
        is_logged_in(params)
        return self.render_template("poslana.html" , params=params)

class TimeHandler(BaseHandler):
    def get(self):
        podatki = "DA"

        user = users.get_current_user()
        emailprejemnika = user.email()
        #todo dej v eno funkcijo ker drugje tudi tole kličem
        seznamrokov = Obletnice.query(Obletnice.pripada == emailprejemnika).fetch()
        for i in range(len(seznamrokov)):
            dan=seznamrokov[i].dan
            mesec=seznamrokov[i].mesec
            rezultat = izracun(dan,mesec)
            seznamrokov[i].doroka=rezultat
        seznamrokov = sorted(seznamrokov, key=lambda dat:dat.doroka, reverse=False)
        params = {"podatki": seznamrokov}

        is_logged_in(params)

        self.render_template("times.html", params=params)



# preko redirecta reseno postanje datumov v tabelo.
class RedirecttimeHandler(BaseHandler):
    def post(self):
        user = users.get_current_user()
        emailprejemnika = user.email()
        rawdt = self.request.get("datum")
        veljavendatum,dan,mesec,leto = vnosdatuma(rawdt)
        #mogoce bi bilo bolje ce bi class naredil in te podatke notri dal - se boljse v bazo pisal locene podatke. sestavil nazaj ce treba. izracun naredil glede na podatke iz baze
        try:
            datum = datetime(leto,mesec,dan)
        except ValueError:
            veljavendatum = "ponovi"
        dogodek = self.request.get("dogodek")
        if (dogodek != "") and veljavendatum == "ok":
            dog = Obletnice(event=dogodek, datum=datum, pripada=emailprejemnika, dan=dan, mesec = mesec, leto=leto, rawdt=rawdt)
            dog.put()
            time.sleep(1)
        #todo: zelo grdo narejen reload strani
        seznamrokov = Obletnice.query(Obletnice.pripada == emailprejemnika).fetch()
        for i in range(len(seznamrokov)):
            dan=seznamrokov[i].dan
            mesec=seznamrokov[i].mesec
            rezultat = izracun(dan,mesec)
            seznamrokov[i].doroka=rezultat
        seznamrokov = sorted(seznamrokov, key=lambda dat:dat.doroka, reverse=False)
        params = {"podatki": seznamrokov, "veljavendatum":veljavendatum}
        is_logged_in(params)
        return self.render_template("times.html" , params=params)

class UganiHandler(BaseHandler):
    def post(self):
        stevilka = self.request.get("poskus")
        is_logged_in(params)
        Random(stevilka,params)
        self.render_template("ugani.html", params=params)


    def get(self):
        podatki = "DA"
        generiraj_random()
        oldseznam = Randomstevilka.query(Randomstevilka.aktivna == True).fetch()
        stevilka=oldseznam[0].zadnjiposkus
        uganil=oldseznam[0].zadnirezultat

        user = users.get_current_user()
        emailprejemnika = user.email()
        params = {"podatki": podatki,"randomnumber":glavna_stevilka,"zadnji":stevilka,"uganil":uganil}
        is_logged_in(params)
        #Random(stevilka,params)
        self.render_template("ugani.html", params=params)


class AdminHandler(BaseHandler):
    def get(self):
        is_logged_in(params)
        seznamuserjev = Uporabniki.query(Uporabniki.vidivse != True).fetch()
        seznamuserjevvseh = Uporabniki.query().fetch()
        posiljatelj = {"prejemniki":seznamuserjev, "vsiprejemniki":seznamuserjevvseh}
        params.update(posiljatelj)
        return self.render_template("admin.html" , params=params)
    def post(self):
        for user in Uporabniki.query(Uporabniki.vidivse != True):
            user.vidivse = True
            user.put()
            time.sleep(1)
        is_logged_in(params)
        seznamuserjev = Uporabniki.query(Uporabniki.vidivse != True).fetch()
        seznamuserjevvseh = Uporabniki.query().fetch()
        posiljatelj = {"prejemniki":seznamuserjev, "vsiprejemniki":seznamuserjevvseh}
        params.update(posiljatelj)
        return self.render_template("admin.html" , params=params)

class WarningHandler(BaseHandler):
    #todo uredi da lahko uporabnik sam izbere kdaj bo obvestilo prišlo
    def get(self):
        #user = users.get_current_user()
        #emailprejemnika = user.email()
        #if emailprejemnika== "podobnik.igor@gmail.com":
        seznamrokov = Obletnice.query().fetch()
        for i in range(len(seznamrokov)):
            dan=seznamrokov[i].dan
            mesec=seznamrokov[i].mesec
            rezultat = izracun(dan,mesec)
            seznamrokov[i].doroka=rezultat
            if rezultat ==7:
                emailprejemnik = seznamrokov[i].pripada
                kvajeto = seznamrokov[i].event
                kdajjeto = seznamrokov[i].rawdt
                mail.send_mail("podobnik.igor@gmail.com", emailprejemnik, "Še 7 dni do dogodka", "Samo da te spomnim, cez 7 dni te caka obletnica od: %s, ki se je zgodil: %s " %(kvajeto,kdajjeto) )
            elif rezultat ==1:
                emailprejemnik = seznamrokov[i].pripada
                kvajeto = seznamrokov[i].event
                kdajjeto = seznamrokov[i].rawdt
                mail.send_mail("podobnik.igor@gmail.com", emailprejemnik, "Še 1 dan do dogodka", "Samo da te spomnim, Jutri te caka obletnica od: %s, ki se je zgodil: %s " %(kvajeto,kdajjeto) )
        return self.render_template("basicredirect.html")

class UnreadHandler(BaseHandler):
    def get(self):
        #user = users.get_current_user()
        #emailprejemnika = user.email()
        #if emailprejemnika== "podobnik.igor@gmail.com":
        newseznam = Sporocilo.query(Sporocilo.new == True).fetch()
        for i in range(len(newseznam)):
            emailprejemnik = newseznam[i].reciever
            mail.send_mail("podobnik.igor@gmail.com", emailprejemnik, "Neprebrana sporočila", "Imas neprebrano sporocilo. Poglej na http://koncniprojekt.appspot.com/")
        return self.render_template("basicredirect.html")


class LestvicaposkusovHandler(BaseHandler):
    def get(self):
        is_logged_in(params)
        lestvicaorig = Randomstevilka.query(Randomstevilka.aktivna == False).fetch()
        lestvicaorig = sorted(lestvicaorig, key=lambda st:st.vposkusih, reverse=False)
        lestvica={"lestvica":lestvicaorig}
        params.update(lestvica)
        return self.render_template("lestvica.html" , params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        is_logged_in(params)
        return self.render_template("posamezno.html" , params=params)

class PosameznoSporociloSendHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        is_logged_in(params)
        return self.render_template("posameznoposlano.html" , params=params)

class PosamezniUserHandler(BaseHandler):
    def get(self, user_id):
        posuser = Uporabniki.get_by_id(int(user_id))
        ##user = Uporabniki.query(Uporabniki.key.id() == user_id).fetch()
        params = {"posuser": posuser}
        is_logged_in(params)
        return self.render_template("posuser.html" , params=params)

class PosamezniUserVidiHandler(BaseHandler):
    def get(self, user_id):
        posuser = Uporabniki.get_by_id(int(user_id))
        posuser.vidivse = True
        posuser.put()
        time.sleep(1)
        ##user = Uporabniki.query(Uporabniki.key.id() == user_id).fetch()
        self.redirect_to("admin1")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/create', CreateHandler),
    webapp2.Route('/mymessages', MyMessagesHandler),
    webapp2.Route('/sendmessages', SendMessagesHandler),
    webapp2.Route('/weather', WeatherHandler),
    webapp2.Route('/redirect', RedirectHandler),
    webapp2.Route('/time', TimeHandler),
    webapp2.Route('/redirecttime', RedirecttimeHandler),
    webapp2.Route('/ugani', UganiHandler),
    webapp2.Route('/admin', AdminHandler, name="admin1"),
    webapp2.Route('/sendwarning', WarningHandler),
    webapp2.Route('/sendunread', UnreadHandler),
    webapp2.Route('/lestvicaugani', LestvicaposkusovHandler),
    webapp2.Route('/mymessages/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/admin/<user_id:\d+>', PosamezniUserHandler),
    webapp2.Route('/admin/<user_id:\d+>/vidi', PosamezniUserVidiHandler),
    webapp2.Route('/sendmessages/<sporocilo_id:\d+>', PosameznoSporociloSendHandler),
], debug=True)
