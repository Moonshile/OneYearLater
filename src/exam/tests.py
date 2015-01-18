
from django.test import TestCase
from django.core.cache import cache

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
                {'content': 'Is #include a macro?', 'level': 0, 'op_ans': [
                    {'content': 'a', 'is_sln': True},
                    {'content': 'b', 'is_sln': False},
                    {'content': 'c', 'is_sln': False},
                    {'content': 'd', 'is_sln': False},
                ]},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
                {'content': 'Is #include a macro?', 'level': 0, 'op_ans': []},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
                {'content': 'Is #include a macro?', 'level': 0, 'op_ans': []},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
                {'content': 'Is #include a macro?', 'level': 0, 'op_ans': []},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
                {'content': 'Is #include a macro?', 'level': 0, 'op_ans': []},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
                {'content': 'Is #include a macro?', 'level': 0, 'op_ans': []},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
            ],
            'question_dist': [{'level': 0, 'count' : 12}, {'level': 3, 'count': 6}],
        }, {
            'name': 'C++',
            'questions': [
                {'content': 'Is #include a macro?', 'level': 1, 'op_ans': []},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
                {'content': 'Is #include a macro?', 'level': 2, 'op_ans': []},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
                {'content': 'Is #include a macro?', 'level': 3, 'op_ans': []},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
                {'content': 'Is #include a macro?', 'level': 4, 'op_ans': []},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
                {'content': 'Is #include a macro?', 'level': 5, 'op_ans': []},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
                {'content': 'Is #include a macro?', 'level': 6, 'op_ans': []},
                {'content': 'Is main() necessary?', 'level': 0, 'op_ans': []},
                {'content': 'What does (*c)(const void *) means?', 'level': 3, 'op_ans': []},
            ],
            'question_dist': [
                {'level': 0, 'count' : 6}, 
                {'level': 1, 'count' : 1}, 
                {'level': 2, 'count' : 1}, 
                {'level': 3, 'count' : 7}, 
                {'level': 4, 'count' : 1}, 
                {'level': 5, 'count' : 1}, 
                {'level': 6, 'count' : 1}, 
            ],
        }, {
            'name': 'Empty',
            'questions': [],
            'question_dist': [],
        },]
    },{
        'name': 'Gaokao',
        'n_first_batch': 12,
        'n_next_batch': 0,
        'n_min': 12,
        'n_max': 12,
        'tags': [],
    },]
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
                for a in q['op_ans']:
                    answer = OptionalAnswer.objects.create(content=a['content'], question=question, is_solution=a['is_sln'])
                    a['id'] = answer.id
    cache.clear()
    return data


