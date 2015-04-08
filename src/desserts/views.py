
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

def desserts(request):
    return render_to_response('desserts.html', RequestContext(request))


