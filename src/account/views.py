
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from goal.forms import GoalForm
from account.models import Account

def addUser(uname, pwd, email, birthday = None, gender = None):
    user = User.objects.create_user(
            username = uname,
            password = pwd,
            email = email,
            )
    user.save()
    account = Account(
            owner = user,
            birthday = birthday,
            gender = gender,
            )
    return user

def addUser(pwd, email, birthday = None, gender = None):
    return addUser(email, pwd, email, birthday, gender)

def addUser(email, birthday = None, gender = None):
    return addUser(email, '', email, birthday, gender)

