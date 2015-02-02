
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie

def index(request):
    return render_to_response('index.html')


