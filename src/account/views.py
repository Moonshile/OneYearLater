
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User

from account.models import Account

def account(request):
    return render_to_response('bowl.html')

def bowl(request):
    return render_to_response('bowl.html')

def dessert(request):
    return render_to_response('dessert.html')

@ensure_csrf_cookie
def signin(request):
    return render_to_response('signin.html')

@ensure_csrf_cookie
def signup(request):
    
    return render_to_response('signup.html')


