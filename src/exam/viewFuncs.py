
from django.core.cache import cache
import random, string, math

from exam import cc
from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from forever.const import RAND_STR_BASE, THETA_NUM

def getOptionalAnswersOfQuestion(question):
    ans = []
    answers = question.optionalanswer_set.all()
    for a in answers:
        new_a = {}
        new_a['id'] = a.id
        new_a['content'] = a.content
        new_a['is_sln'] = a.is_solution
        ans.append(new_a)
    return ans

def getQuestionsInTag(tag):
    qs = []
    questions = tag.question_set.all()
    for q in questions:
        new_q = {}
        new_q['id'] = q.id
        new_q['content'] = q.content
        new_q['level'] = q.level
        new_q['op_ans'] = getOptionalAnswersOfQuestion(q)
        qs.append(new_q)
    return qs

def getTagsInCategory(category):
    ts = []
    tags = category.tag_set.all()
    for t in tags:
        new_t = {}
        new_t['id'] = t.id
        new_t['name'] = t.name
        new_t['questions'] = getQuestionsInTag(t)
        new_t['question_dist'] = t.questionDistribution()
        ts.append(new_t)
    return ts

# must guarantee that the category name exists
def getCachedCategory(category_name):
    key = cc.CATEGORY_BASE + category_name
    category = cache.get(key)
    # if in cache
    if category:
        return category
    # not in cache
    cs = Category.objects.filter(name=category_name)
    if cs.count() == 0:
        return None
    c = cs[0]
    category = {'id': c.id, 'name': c.name, 
        'n_first_batch': c.n_first_batch, 'n_next_batch': c.n_next_batch,
        'n_min': c.n_min, 'n_max': c.n_max,
        'v_step': c.v_step, 'v_base': c.v_base, 'free_time': c.free_time, 'max_time': c.max_time,
        'tags': getTagsInCategory(c)
    }
    cache.set(key, category)
    return category

# get a dict that map tags to their categories
def getCachedTagCategoryMap():
    m = cache.get(cc.TAG_CATEGORY_MAP)
    if m:
        return m
    tags = Tag.objects.all()
    m = {}
    for t in tags:
        m[t.name] = t.category.name
    cache.set(cc.TAG_CATEGORY_MAP, m)
    return m

def getCachedOptionalAnswers():
    op_ans = cache.get(cc.OPTIONAL_ANSWERS)
    if op_ans:
        return op_ans
    answers = OptionalAnswer.objects.all()
    op_ans = {}
    for a in answers:
        op_ans[a.id] = {}
        op_ans[a.id]['is_sln'] = a.is_solution
        op_ans[a.id]['qid'] = a.question.id
    cache.set(cc.OPTIONAL_ANSWERS, op_ans)
    return op_ans

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


