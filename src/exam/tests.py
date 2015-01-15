
from django.test import TestCase

from exam.models import *

def commonSetUp():
    data = [{
        'name': 'Programmer',
        'tags': [{
            'name': 'C', 
            'questions': [
                {'content': 'Is #include a macro?', 'level': 0},
                {'content': 'Is main() necessary?', 'level': 0},
                {'content': 'What does (*c)(const void *) means?', 'level': 3},
            ]
        },{
            'name': 'C++',
            'questions': [],
        }]
    },{
        'name': 'Gaokao',
        'tags': [],
    }]
    for c in data:
        category = Category.objects.create(name=c['name'])
        c['id'] = category.id
        for t in c['tags']:
            tag = Tag.objects.create(name=t['name'], category=category)
            t['id'] = tag.id
            for q in t['questions']:
                question = Question.objects.create(content=q['content'], level=q['level'], tag=tag)
                q['id'] = question.id
    return data


