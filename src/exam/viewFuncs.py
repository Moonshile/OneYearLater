
from django.core.cache import cache
import random, string

from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from forever.const import RAND_STR_BASE

def getQuestionsInTag(tag):
    qs = []
    questions = tag.question_set.all()
    for q in questions:
        new_q = {}
        new_q['id'] = q.id
        new_q['content'] = q.content
        new_q['level'] = q.level
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
    key = 'category' + category_name
    category = cache.get(key)
    # if in cache
    if category:
        return category
    # not in cache
    cs = Category.objects.filter(name=category_name)
    if len(cs) == 0:
        return None
    c = cs[0]
    category = {'id': c.id, 'name': c.name, 
        'n_first_batch': c.n_first_batch, 'n_next_batch': c.n_next_batch,
        'n_min': c.n_min, 'n_max': c.n_max,
        'tags': getTagsInCategory(c)
    }
    cache.set(key, category)
    return category

# get a dict that map tags to their categories
def getCachedTagCategoryMap():
    key = 'tag_category_map'
    m = cache.get(key)
    if m:
        return m
    tags = Tag.objects.all()
    m = {}
    for t in tags:
        m[t.name] = t.category.name
    cache.set(key, m)
    return m

# generate a 6-charater random string
def genQtoken():
    return string.join(random.sample(RAND_STR_BASE, 6)).replace(' ' , '')

