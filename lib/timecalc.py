__author__ = 'Igor'
import datetime
import relativedelta





def razlika(ime):
    now = datetime.now()
    a = relativedelta(now,ime)
    return a




"""
koncno = razlika(igor)
print koncno.years
print koncno.months
print koncno.days
igor = datetime(1983, 5, 6, 9, 45)
marusa = datetime(1984, 5, 4, 12, 00)
now = datetime.now()
today = date.today()
"""