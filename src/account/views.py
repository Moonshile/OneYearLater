#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from django.contrib import auth
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
    if request.method == 'POST':
        form = SigninForm(request.POST)
        err = None
        if form.is_valid():
            cd = form.cleaned_data
            user = auth.authenticate(
                email = cd['username'],
                password = cd['password'],
            ) or auth.authenticate(
                username = cd['username'],
                password = cd['password'],
            )
            if user is not None:
                request.session.set_expiry(None)
                # TODO
                return render_to_response('signin.html', RequestContext(request))
            err = {'total': [u'用户名或密码错误']}
        else:
            err = form.errors
        return render_to_response('signin.html', RequestContext(request, {'err': err}))
    else:
        return render_to_response('signin.html', RequestContext(request))

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
            # TODO
            return render_to_response('signup.html', RequestContext(request))
        return render_to_response('signup.html', RequestContext(request, {'err': form.errors}))
    else:
        return render_to_response('signup.html', RequestContext(request))


