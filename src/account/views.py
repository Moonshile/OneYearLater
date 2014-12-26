
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from goal.forms import GoalForm

def addUser(uname, pwd, email):
    user = User.objects.create_user(
            username = uname,
            password = pwd,
            email = email,
            )
    user.save()
    return user

def addUser(pwd, email):
    return addUser(email, pwd, email)

def addUser(email):
    return addUser(email, '', email)
