
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
import random, string

from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from exam.viewFuncs import getCachedCategory, genQtoken, nextQuestions
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
    request.session['c_name'] = request.GET['c']
    return JsonResponse(res)

def getQuestions(request):
    q_token_name = 'q_token'
    q_token = request.session.get(q_token_name, None)
    q_token_get = request.GET['q_token'] if 'q_token' in request.GET else None
    # wrong q_token: forbidden
    if not q_token or q_token != q_token_get or 'c_name' not in request.session:
        raise PermissionDenied
    count = request.session.get(q_token, 0)
    # q_token bound with 0: not found
    if count == 0:
        raise Http404
    tag = request.GET['t'] if 't' in request.GET else None
    level = request.GET['l'] if 'l' in request.GET else None
    category = getCachedCategory(request.session['c_name'])
    qids = request.session.get('qids', [])
    # get randomly not repeated questions with certain tag, level and count
    qs = nextQuestions(qids, category, tag, level, count)
    qids += map(lambda x: x['id'], qs)
    q_token = genQtoken()
    enough_correct = len(request.session.get('answers', [])) >= category['n_min']
    enough_questions = len(qids) >= category['n_max']
    no_more = reduce(lambda res, t: res + len(t['questions']), category['tags'], 0) <= len(qids)
    res = {
        'err_code': err['OK'].code,
        'err_msg': err['OK'].msg,
        q_token_name: q_token,
        'has_next': False if enough_correct or enough_questions or no_more else True,
        'questions': qs,
    }
    # update sessions
    request.session[q_token_name] = q_token
    request.session[q_token] = category['n_next_batch'] if res['has_next'] else 0
    request.session['qids'] = qids
    return JsonResponse(res)

def handInAnswer(request):
    res = {
        'err_code': 0,
        'err_msg': '',
    }
    return JsonResponse(res)

def finishAnswer(request):
    res = {
        'err_code': 0,
        'err_msg': '',
        'rank': {'No.': 1, 'rate': .9},
        'answer_sheet': {'token': '', id: '', 'score': 0},
        'share_url': '',
    }
    return JsonResponse(res)


