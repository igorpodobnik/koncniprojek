# coding=utf-8
__author__ = 'Igor'
from google.appengine.api import users
from lib.models import Uporabniki,Sporocilo
from google.appengine.ext import ndb
from google.appengine.api import mail
import time

def is_logged_in(P):
    user = users.get_current_user()
    Pint = P
    if user:
        stevilonovih = 0
        steviloposlanih = 0
        logiran = True
        logout_url = users.create_logout_url('/')
        preverialiobstaja()
        approved=preveriapproved()
        paramsif = {"logiran": logiran, "logout_url": logout_url, "user": user,"approved":approved}
        Pint.update(paramsif)
        ## samo poslji mejl ce se ne
        emailprejemnika = user.email()
        for novih in Sporocilo.query(ndb.AND(Sporocilo.reciever == emailprejemnika,Sporocilo.new == True)):
            stevilonovih +=1
        novihje = {"stnovih":stevilonovih}
        Pint.update(novihje)
        for starih in Sporocilo.query(ndb.AND(Sporocilo.sender == emailprejemnika,Sporocilo.new == True)):
            steviloposlanih +=1
        starihje = {"stposlanih":steviloposlanih}
        Pint.update(starihje)
        if emailprejemnika == "podobnik.igor@gmail.com":
            adminuser = {"admin": "da"}
        else:
            adminuser = {"admin": "ne"}
        Pint.update(adminuser)
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
    prisoten = Uporabniki.query(Uporabniki.user == emailprejemnika).fetch()
    if prisoten:
        print "NOTRI JE ZE!"
    else:
        user.put()
        time.sleep(2)
        mail.send_mail("podobnik.igor@gmail.com", "podobnik.igor@gmail.com", "Nov uporabnik", "Novega userja imaš in sicer %s" %emailprejemnika)

def preveriapproved():
    user = users.get_current_user()
    emailprejemnika = user.email()
    check=Uporabniki.query(ndb.AND(Uporabniki.user == emailprejemnika,Uporabniki.approved == True)).fetch()

    if check:
        rezultat = "da"
    else:
        rezultat = "ne"
    return rezultat

def preverividivse():
    user = users.get_current_user()
    emailprejemnika = user.email()
    check=Uporabniki.query(ndb.AND(Uporabniki.user == emailprejemnika,Uporabniki.vidivse == True)).fetch()

    if check:
        vidi = "da"
    else:
        vidi = "ne"
    return vidi