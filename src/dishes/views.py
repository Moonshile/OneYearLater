
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

def dishes(request):
    return render_to_response('dishes.html', RequestContext(request))

def dishDetail(request, dish_id):
    return render_to_response('dish-detail.html', RequestContext(request))

