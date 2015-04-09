#coding=utf-8
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from forms import AddActivityForm, RmActivityForm
from models import Activity, Dessert

def desserts(request):
    return render_to_response('desserts.html', RequestContext(request))

def bowl(request):
    if request.user.is_authenticated():
        print request.user.activity_set.all()
        return render_to_response('dessert-bowl.html', RequestContext(request, {
            'activities': request.user.activity_set.all(),
        }))
    return render_to_response('dessert-bowl.html', RequestContext(request))

@require_http_methods(['POST'])
@login_required()
def add(request):
    form = AddActivityForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if Activity.objects.filter(text=cd['text']).count() > 0:
            return JsonResponse({'success': True})
        a = Activity.objects.create(owner=request.user, text=cd['text'])
        return JsonResponse({'success': True, 'data': {'id': a.id}})
    return JsonResponse({'success': False, 'data': form.errors})

@require_http_methods(['POST'])
@login_required()
def remove(request):
    form = RmActivityForm(request.POST)
    if form.is_valid():
        cd = cleaned_data
        Activity.objects.filter(id=cd['id']).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'data': form.errors})

@require_http_methods(['POST'])
@login_required()
def todo(request):
    return JsonResponse({'success': False, 'data': form.errors})

@require_http_methods(['POST'])
@login_required()
def done(request):
    return JsonResponse({'success': False, 'data': form.errors})

