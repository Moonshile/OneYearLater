
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie

def dishes(request):
    return render_to_response('dishes.html')

def dishDetail(request, dish_id):
    return render_to_response('dish-detail.html')

