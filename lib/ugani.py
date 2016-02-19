__author__ = 'Franko'
from google.appengine.ext import ndb
from lib.models import Randomstevilka
from datetime import datetime
import time
import random
from google.appengine.api import users

def Random(stevilka,params):
        R=params
        #samo kontrola
        alijerandom=preveri_random()
        stevilka=int(stevilka)
        glavna_stevilka= generiraj_random()
        glavna_stevilka=int(glavna_stevilka)
        if stevilka < glavna_stevilka:
            tekst = "up"
        elif stevilka > glavna_stevilka:
            tekst = "down"
        else:
            tekst = "ok"
            for user in Randomstevilka.query(Randomstevilka.aktivna == True):
                user.aktivna = False
                user.put()
        stposkusov=povecaj_poskuse(stevilka,tekst)
        parametri={"random":alijerandom,"randomnumber":glavna_stevilka, "uganil":tekst,"zadnji":stevilka,"stposkusov":stposkusov}
        R.update(parametri)
        return R

def preveri_random():
        oldseznam = Randomstevilka.query(Randomstevilka.aktivna == True).fetch()
        if oldseznam:
            alfa = True
        else:
            alfa = False
        return alfa


def generiraj_random():
        beta = random.randrange(0,10000,1)
        kontrola = preveri_random()
        if kontrola == False:
            nova_random = Randomstevilka(stevilo=beta)
            nova_random.put()
            time.sleep(1)
        else:
            oldseznam = Randomstevilka.query(Randomstevilka.aktivna == True).fetch()
            beta=oldseznam[0].stevilo
        return beta

def povecaj_poskuse(ugib,updown):
    user = users.get_current_user()
    emailprejemnika = user.email()
    for user in Randomstevilka.query(Randomstevilka.aktivna == True):
        user.vposkusih += 1
        user.zadnjiposkus = ugib
        user.zadnirezultat = updown
        user.uganil = emailprejemnika
        user.put()
    return user.vposkusih

