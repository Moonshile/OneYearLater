
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from goal.forms import GoalForm
from goal.models import Goal
from account import views as Account
from datetime import date, timedelta

@ensure_csrf_cookie
def index(request):
    return render_to_response('goal.html')

def addGoal(request):
    if request.method != 'POST':
        return render_to_response('json/simple_res.json', 
                {'success': False, 'errs': ['post'], })
    form = GoalForm(request.POST)
    if not form.is_valid():
        return render_to_response('json/simple_res.json',
                {'success': False, 'errs': form.errors.keys()})
    email = form.cleaned_data['email']
    content = form.cleaned_data['content']
    age = form.cleaned_data['age']
    gender = form.cleaned_data['gender']
    user = User.objects.filter(username=email)
    if not user:
        user = Account.addUser(
                username = email, 
                age = age, 
                gender = gender,
                )
    else:
        user = user[0]
    goal = Goal(
            content = content,
            ip = request.META['REMOTE_ADDR'],
            author = user,
            )
    goal.save()
    return render_to_response('json/simple_res.json', {'success': True})

def countGoals(request):
    return render_to_response('json/number.json', 
            {'success': True, 'num': Goal.objects.count()})

