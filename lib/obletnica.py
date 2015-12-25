__author__ = 'Franko'
import datetime
import relativedelta

from datetime import *; from relativedelta import *



prva = 1
druga = 2
tretja = 3
cetrta = 4
peta = 5
c="."


def izracun(dan,mesec):
    today = date.today()
    obletnica = date(today.year,mesec,dan)
    koliko = obletnica - today

    if koliko.days < 0:
        novoleto = today.year + 1
        obletnica=date(novoleto,mesec,dan)

    koliko = obletnica - today
    return koliko.days

def izracunrojdneva(ime):
    today = date.today()
    obletnica = ime
    obletnica=date(today.year,obletnica.month,obletnica.day)
    koliko = obletnica - today


    if koliko.days < 0:
        novoleto = today.year + 1
        obletnica=date(novoleto,obletnica.month,obletnica.day)
    koliko = obletnica - today
    return koliko.days


def vnosdatuma(datum):
    rezultat="ok"
    pozicije=[pos for pos, char in enumerate(datum) if char == c]
    if prva in pozicije:
        if tretja in pozicije:
            dan = int(datum[:1])
            mesec = int(datum[2:3])
            leto = int(datum[4:8])
        elif cetrta in pozicije:
            dan = int(datum[:1])
            mesec = int(datum[2:4])
            leto = int(datum[5:9])
        else:
            rezultat = "ponovi"
    elif druga in pozicije:
        if peta in pozicije:
            dan = int(datum[:2])
            mesec = int(datum[3:5])
            leto = int(datum[6:10])
        elif cetrta in pozicije:
            dan = int(datum[:2])
            mesec = int(datum[3:4])
            leto = int(datum[5:9])
        else:
            rezultat = "ponovi"
    else:
        rezultat = "ponovi"

    return rezultat,dan,mesec,leto


