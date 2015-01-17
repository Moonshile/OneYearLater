
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
import random, string

from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from exam.viewFuncs import getCachedCategory, genQtoken
from forever.const import err, RAND_STR_BASE, REQ_FREQUENCY_LIMIT
from forever.settings import DEBUG

def index(request):
    pass

def getTags(request):
    # deal with too frequent requests from a user
    ssid = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
    cached_freq = cache.get(ssid, 0)
    if cached_freq and cached_freq >= REQ_FREQUENCY_LIMIT:
        cache.set(ssid, cached_freq, 2 if DEBUG else 3600) # forbid access in 1 hour
        raise PermissionDenied
    else:
        cached_freq += 1
    cache.set(ssid, cached_freq, 1 if DEBUG else 300) # cache for 300 seconds
    # begin to get the tags
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
    request.session[q_token] = category['n_first_batch']
    return JsonResponse(res)

def getQuestions(request):
    res = {}
    return JsonResponse(res)

def handInAnswer(request):
    res = {}
    return JsonResponse(res)

def finishAnswer(request):
    res = {}
    return JsonResponse(res)


