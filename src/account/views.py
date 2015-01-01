
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from goal.forms import GoalForm
from account.models import Account

def addUser(username, pwd=None, email=None, age=None, gender=None):
    user = User.objects.create_user(
            username = username,
            password = username if pwd is None else pwd,
            email = username if email is None else email,
            )
    user.save()
    addAccount(user, age, gender)
    return user

def addAccount(owner, age=None, gender=None):
    account = Account(
            owner = owner,
            age = age,
            gender = gender,
            )
    account.save()
    return account


