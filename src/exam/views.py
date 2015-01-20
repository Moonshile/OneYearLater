
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.conf import settings
import random, string

from exam import ss, cc
from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from exam.viewFuncs import *
from exam.forms import *
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
    res = {
        'err_code': err['OK'].code,
        'err_msg': err['OK'].msg,
        'tags': map(lambda t: {'name': t['name'], 'question_dist': t['question_dist']}, tags),
        'q_token': q_token
    }
    # put q_token into session, 
    # and when request for questions, put question id as key into session with current q_token as value
    request.session[ss.Q_TOKEN] = q_token
    request.session[q_token] = category['n_first_batch']
    request.session[ss.CATEGORY_NAME] = request.GET['c']
    return JsonResponse(res)

def getQuestions(request):
    q_token = request.session.get(ss.Q_TOKEN, None)
    q_token_get = request.GET.get('q_token', None)
    # wrong q_token: forbidden
    if not q_token or q_token != q_token_get or ss.CATEGORY_NAME not in request.session:
        raise PermissionDenied
    count = request.session.get(q_token, 0)
    # q_token bound with 0: not found
    if count == 0:
        raise Http404
    q_token = genQtoken()
    tag = request.GET.get('t', None)
    level = request.GET.get('l', None)
    category = getCachedCategory(request.session[ss.CATEGORY_NAME])
    qids = request.session.get(ss.QUESTION_IDS, {})
    # get randomly not repeated questions with certain tag, level and count
    qs = nextQuestions(qids, category, tag, level, count)
    for q in qs:
        qids[q['id']] = (q_token, q['level'])
    enough_correct = len(request.session.get(ss.ANSWERS, [])) >= category['n_min']
    enough_questions = len(qids) >= category['n_max']
    no_more = reduce(lambda res, t: res + len(t['questions']), category['tags'], 0) <= len(qids)
    res = {
        'err_code': err['OK'].code,
        'err_msg': err['OK'].msg,
        'q_token': q_token,
        'has_next': False if enough_correct or enough_questions or no_more else True,
        'questions': qs,
    }
    # update sessions
    request.session[ss.Q_TOKEN] = q_token
    request.session[q_token] = category['n_next_batch'] if res['has_next'] else 0
    request.session[ss.QUESTION_IDS] = qids
    return JsonResponse(res)

@require_http_methods(['POST'])
def handInAnswer(request):
    cached_op_ans = getCachedOptionalAnswers()
    qids = request.session[ss.QUESTION_IDS]
    form = HandInAnswerForm(request.POST, cached_op_ans, qids)
    if not form.is_valid():
        return JsonResponse({
            'err_code': err['ERROR'].code, 
            'err_msg': map(lambda x: x + ' ' + err['ERROR'].msg, form.errors.keys())
        })
    ans = request.session.get(ss.ANSWERS, [])
    cd = form.cleaned_data
    cached_ans = cached_op_ans[cd['id']]
    ans.append({
        'id': cd['id'], 
        'time': cd['time'], 
        'is_sln': cached_ans['is_sln'],
        'level': qids[cached_ans['qid']][1]
    })
    request.session[ss.ANSWERS] = ans
    return JsonResponse({'err_code': err['OK'].code, 'err_msg': err['OK'].msg})

@require_http_methods(['POST'])
def finishAnswer(request):
    form = FinishAnswerForm(request.POST, request.session)
    if not form.is_valid():
        raise PermissionDenied
    user = request.user if request.user.is_authenticated() else None
    category = getCachedCategory(request.session[ss.CATEGORY_NAME])
    answers = request.session.get(ss.ANSWERS, [])
    token = genQtoken(8)
    while AnswerSheet.objects.filter(token=token).count() > 0:
        token = genQtoken(8)
    answer_sheet = AnswerSheet.objects.create(owner=user, token=token, score=computeScore(category, answers))
    for a in answers:
        Answer.objects.create(answer_sheet=answer_sheet, choosed_answer_id=a['id'], cost_time=a['time'])
    rank = AnswerSheet.objects.filter(score__lte=answer_sheet.score).count()
    total = AnswerSheet.objects.count()
    res = {
        'err_code': err['OK'].code,
        'err_msg': err['OK'].msg,
        'rank': {'No.': rank, 'ratio': computeRatio(rank, total, answer_sheet.score)},
        'answer_sheet': {'token': answer_sheet.token, 'score': answer_sheet.score},
    }
    return JsonResponse(res)

def queryAnswerSheet(request):
    pass


def share(request):
    pass


