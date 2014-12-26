
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from goal.forms import GoalForm
from goal.models import Goal
from account import views as Account

def index(request):
    return render_to_response('goal.html')

@ensure_csrf_cookie
def addGoal(request):
    if request.method != 'POST':
        return render_to_response('json/simple_res.json', 
                RequestContext(request, {'success': False, 'errs': ['post'], }))
    form = GoalForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        content = form.cleaned_data['content']
        user = Account.addUser(email)
        goal = Goal(
                content = content,
                ip = request.META.REMOTE_ADDR,
                author = useri
                )
        goal.save()
        return render_to_response('json/simple_res.json', RequestContext(request, {'success': True}))
    return render_to_response('json/simple_res.json',
            RequestContext(request, {'success': False, 'errs': form.errors.keys()}))

