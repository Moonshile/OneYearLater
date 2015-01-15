
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import ensure_csrf_cookie
import random, string

from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from forever.const import err, RAND_STR_BASE

def index(request):
    pass

def genQtoken():
    return string.join(random.sample(RAND_STR_BASE, 6)).replace(' ' , '')

def getTags(request):
    # TODO deal with cache
    categories = Category.objects.filter(name=request.GET['c'])
    if(len(categories) == 0):
        return JsonResponse({'err_code': err['NOT_EXIST'].code, 'err_msg': [u'category ' + err['NOT_EXIST'].msg]})
    tags = categories[0].tag_set.all()
    q_token = genQtoken()
    q_token_name = 'q_token'
    res = {
        'err_code': err['OK'].code,
        'err_msg': err['OK'].msg,
        'tags': map(lambda t: t.questionDistribution(), tags),
        q_token_name: q_token
    }
    # put q_token into session
    if request.session.has_key(q_token_name):
        request.session[q_token_name].append(q_token)
    else:
        request.session[q_token_name] = [q_token]
    return JsonResponse(res)

def getQuestions(request):
    pass

def handInAnswer(request):
    pass

def finishAnswer(request):
    pass


