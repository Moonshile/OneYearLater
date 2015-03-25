#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from django.contrib.auth.models import User

from models import Account
from forms import SignupForm, SigninForm

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
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                username = cd['username'],
                password = cd['password'],
                email = cd['email'],
            )
            user.save()
            account = Account(owner=user)
            account.save()
            return render_to_response('signup.html', RequestContext(request))
        return render_to_response('signup.html', RequestContext(request, {'err': form.errors}))
    else:
        return render_to_response('signup.html', RequestContext(request))


