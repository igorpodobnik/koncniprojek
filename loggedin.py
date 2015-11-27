__author__ = 'Igor'
from google.appengine.api import users
from models import Uporabniki,Sporocilo
from google.appengine.ext import ndb



def is_logged_in(P):
    user = users.get_current_user()
    Pint = P
    if user:
        stevilonovih = 0
        logiran = True
        logout_url = users.create_logout_url('/')
        print "glej gor"
        paramsif = {"logiran": logiran, "logout_url": logout_url, "user": user}
        Pint.update(paramsif)
        preverialiobstaja()
        emailprejemnika = user.email()
        for novih in Sporocilo.query(ndb.AND(Sporocilo.reciever == emailprejemnika,Sporocilo.new == True)):
            stevilonovih +=1
        params1 = {"stnovih":stevilonovih}
        Pint.update(params1)
    else:
        logiran = False
        login_url = users.create_login_url('/')
        paramsif = {"logiran": logiran, "login_url": login_url, "user": user}
        Pint.update(paramsif)

    return Pint

def preverialiobstaja():
    user = users.get_current_user()
    emailprejemnika = user.email()
    user = Uporabniki(user=emailprejemnika)
    # preverjam ce je user ze v bazi
    prisoten = Uporabniki.query(Uporabniki.user==emailprejemnika).fetch()

    if prisoten:
        print "NOTRI JE ZE!"
    else:
        user.put()
