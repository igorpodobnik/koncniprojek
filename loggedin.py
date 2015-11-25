__author__ = 'Igor'
from google.appengine.api import users

def is_logged_in(P):
    user = users.get_current_user()
    Pint = P
    if user:
        logiran = True
        logout_url = users.create_logout_url('/')
        print user.nickname()
        print user.user_id()
        print "glej gor"
        paramsif = {"logiran": logiran, "logout_url": logout_url, "user": user}
        Pint.update(paramsif)
    else:
        logiran = False
        login_url = users.create_login_url('/')
        paramsif = {"logiran": logiran, "login_url": login_url, "user": user}
        Pint.update(paramsif)
    return Pint