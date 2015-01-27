
from django.core.cache import cache
import random, string, math

from exam import cc
from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from forever.const import RAND_STR_BASE, THETA_NUM

# decorator to cache returned value of func with key
def with_cache(key):
    def decorator(func):
        def inner(*args):
            value = cache.get(key)
            if value:
                return value
            value = func(*args)
            cache.set(key, value)
            return value
        return inner
    return decorator

@with_cache(cc.OPTIONAL_ANS)
def getCachedOptionalAnswers():
    ans = {}
    answers = OptionalAnswer.objects.all()
    for a in answers:
        ans[a.id] = {
            'content': a.content,
            'qid': a.question.id,
            'is_sln': a.is_solution,
        }
    return ans

@with_cache(cc.QUESTIONS)
def getCachedQuestions():
    qs = {}
    questions = Question.objects.all()
    ans = getCachedOptionalAnswers()
    for q in questions:
        qs[q.id] = {
            'content': q.content,
            'tid': q.tag.id,
            'level': q.level,
            'op_ans': filter(lambda a: ans[a]['qid'] == q.id, ans.keys()),
        }
    return qs

@with_cache(cc.TAGS)
def getCachedTags():
    ts = {}
    tags = Tag.objects.all()
    questions = getCachedQuestions()
    for t in tags:
        ts[t.id] = {
            'name': t.name,
            'cid': t.category.id,
            'questions': filter(lambda q: questions[q]['tid'] == t.id, questions.keys()),
            'question_dist': t.questionDistribution(),
        }
    return ts

@with_cache(cc.CATEGORIES)
def getCachedCategories():
    cs = {}
    categories = Category.objects.all()
    tags = getCachedTags()
    for c in categories:
        cs[c.name] = {
            'id': c.id,
            'n_min': c.n_min,
            'n_max': c.n_max,
            'v_step': c.v_step,
            'v_base': c.v_base,
            'free_time': c.free_time,
            'max_time': c.max_time,
            'tags': filter(lambda t: tags[t]['cid'] == c.id, tags.keys()),
        }
    return cs

# generate a 6-charater random string
def genQtoken(length=6):
    return string.join(random.sample(RAND_STR_BASE, length)).replace(' ' , '')

def nextQuestionsWithRandomTagLevel(qids, category, count):
    questions = reduce(
        lambda res, x: res + filter(
            lambda x: x['id'] not in qids,
            x['questions']
        ),
        category['tags'],
        []
    )
    if len(questions) <= count:
        return questions
    return random.sample(questions, count)

def nextQuestionsWithRandomTag(qids, category, level, count):
    questions = reduce(
        lambda res, x: res + filter(
            lambda x: x['level'] == level and x['id'] not in qids,
            x['questions']
        ),
        category['tags'],
        []
    )
    if len(questions) <= count:
        return questions
    return random.sample(questions, count)

def nextQuestionsWithRandomLevel(qids, category, tag, count):
    questions = filter(
        lambda q: q['id'] not in qids,
        reduce(
            lambda res, t: res + t['questions'],
            filter(lambda t: t['name'] == tag, category['tags']),
            []
        )
    )
    if len(questions) <= count:
        return questions
    return random.sample(questions, count)

def nextQuestionsWithFixedTagLevel(qids, category, tag, level, count):
    questions = filter(
        lambda q: q['level'] == level and q['id'] not in qids,
        reduce(
            lambda res, t: res + t['questions'],
            filter(lambda t: t['name'] == tag, category['tags']),
            []
        )
    )
    if len(questions) <= count:
        return questions
    return random.sample(questions, count)

"""
generate next not repeated questions randomly
"""
def nextQuestions(qids, category, tag=None, level=None, count=1):
    if tag is None and level is None:
        return nextQuestionsWithRandomTagLevel(qids, category, count)
    if tag is None:
        return nextQuestionsWithRandomTag(qids, category, level, count)
    if level is None:
        return nextQuestionsWithRandomLevel(qids, category, tag, count)
    return nextQuestionsWithFixedTagLevel(qids, category, tag, level, count)

"""
compute score
"""
def computeScore(category, ans):
    step = category['v_step']
    base = category['v_base']
    free_time = category['free_time']
    max_time = category['max_time']
    score = 0.0
    for a in ans:
        time = 0 if a['time'] < free_time else (max_time if max_time < a['time'] else a['time'] - free_time)
        score += (step*a['level'] + base)*math.exp(-0.05*(time if a['is_sln'] else 2*max_time))
    return score

"""
compute ratio of scores lower than a score
"""
SAL_DIST = filter(lambda x: x >= 5 and x <= 100, map(lambda x: int(random.normalvariate(15, 15)), range(0,1000)))
def computeRatio(rank, total, score):
    if total > THETA_NUM:
        return rank/float(total)
    return len(filter(lambda x: x <= score, SAL_DIST))/float(len(SAL_DIST))


