#coding=utf-8
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from django.contrib import auth
from django.contrib.auth.models import User

from models import Account
from forms import SignupForm, SigninForm

def account(request):
    return render_to_response('bowl.html', RequestContext(request))

def bowl(request):
    return render_to_response('bowl.html', RequestContext(request))

def dessert(request):
    return render_to_response('dessert.html', RequestContext(request))

@ensure_csrf_cookie
@require_http_methods(['POST'])
def signout(request):
    auth.logout(request)
    return redirect(request.GET.get('next', '/'))

@ensure_csrf_cookie
def signin(request):
    if request.user.is_authenticated():
        return redirect(reverse(bowl))
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
            if user is not None and user.is_active:
                request.session.set_expiry(None)
                auth.login(request, user)
                print request.GET.get('next', reverse(bowl))
                return redirect(request.GET.get('next', reverse(bowl)))
            err = {'total': [u'用户名或密码错误']}
        else:
            err = form.errors
        return render_to_response('signin.html', RequestContext(request, {'err': err}))
    else:
        is_new = request.GET.get('new', False)
        return render_to_response('signin.html', RequestContext(request, {'new': is_new}))

@ensure_csrf_cookie
def signup(request):
    if request.user.is_authenticated():
        return redirect(reverse(bowl))
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
            nxt = request.GET.get('next', '')
            args = '?new=true&next=' + nxt if nxt else '?new=true'
            return redirect(reverse(signin) + args)
        return render_to_response('signup.html', RequestContext(request, {'err': form.errors}))
    else:
        return render_to_response('signup.html', RequestContext(request))


