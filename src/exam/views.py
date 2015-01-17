
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import ensure_csrf_cookie
import random, string

from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from exam.viewFuncs import getCachedCategory, genQtoken
from forever.const import err, RAND_STR_BASE

def index(request):
    pass

def getTags(request):
    # TODO deal with to frequent requests from a user
    category = getCachedCategory(request.GET['c'])
    if(not category):
        return JsonResponse({'err_code': err['NOT_EXIST'].code, 'err_msg': [u'category ' + err['NOT_EXIST'].msg]})
    tags = category['tags']
    q_token = genQtoken()
    q_token_name = 'q_token'
    res = {
        'err_code': err['OK'].code,
        'err_msg': err['OK'].msg,
        'tags': map(lambda t: {'name': t['name'], 'question_dist': t['question_dist']}, tags),
        q_token_name: q_token
    }
    # put q_token into session, 
    # and when request for questions, put question id as key into session with current q_token as value
    request.session[q_token_name] = q_token
    return JsonResponse(res)

def getQuestions(request):
    pass

def handInAnswer(request):
    pass

def finishAnswer(request):
    pass


