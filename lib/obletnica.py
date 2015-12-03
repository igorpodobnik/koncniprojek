__author__ = 'Franko'
import datetime
import relativedelta

from datetime import *; from relativedelta import *




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

