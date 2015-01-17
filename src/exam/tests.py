
from django.test import TestCase

from exam.models import *

def commonSetUp():
    data = [{
        'name': 'Programmer',
        'n_first_batch': 5,
        'n_next_batch': 1,
        'n_min': 10,
        'n_max': 15,
        'tags': [{
            'name': 'C', 
            'questions': [
                {'content': 'Is #include a macro?', 'level': 0},
                {'content': 'Is main() necessary?', 'level': 0},
                {'content': 'What does (*c)(const void *) means?', 'level': 3},
            ],
            'question_dist': [{'level': 0, 'count' : 2}, {'level': 3, 'count': 1}],
        },{
            'name': 'C++',
            'questions': [],
            'question_dist': [],
        }]
    },{
        'name': 'Gaokao',
        'n_first_batch': 12,
        'n_next_batch': 0,
        'n_min': 12,
        'n_max': 12,
        'tags': [],
    }]
    for c in data:
        category = Category.objects.create(name=c['name'], n_min=c['n_min'], n_max=c['n_max'],
            n_first_batch=c['n_first_batch'], n_next_batch=c['n_next_batch']
        )
        c['id'] = category.id
        for t in c['tags']:
            tag = Tag.objects.create(name=t['name'], category=category)
            t['id'] = tag.id
            for q in t['questions']:
                question = Question.objects.create(content=q['content'], level=q['level'], tag=tag)
                q['id'] = question.id
    return data


