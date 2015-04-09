#coding=utf-8
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

def dishes(request):
    return render_to_response('dishes.html', RequestContext(request))

def dishDetail(request, dish_id):
    return render_to_response('dish-detail.html', RequestContext(request))

@login_required()
def bowl(request):
    return render_to_response('dish-bowl.html', RequestContext(request))
