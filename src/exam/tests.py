
from django.test import TestCase
from django.core.cache import cache
import copy, random, string

from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from forever import const

def commonSetUp(self):
    categories =  {
        'Programmer': {
            'n_min': 10,
            'n_max': 15,
            'v_step': 2,
            'v_base': 3,
            'free_time': 10,
            'max_time': 32,
        },
        'Gaokao': {
            'n_min': 15,
            'n_max': 15,
            'v_step': 1,
            'v_base': 5,
            'free_time': 8,
            'max_time': 18,
        },
        'empty': {
            'n_min': 15,
            'n_max': 15,
            'v_step': 1,
            'v_base': 5,
            'free_time': 8,
            'max_time': 18,
        },
    }
    tags = {}
    questions = {}
    op_ans = {}
    base = '1234567890qazwsxcderfvbgtyhnmjuiklop, .?'
    def genName():
        return string.join(random.sample(base, random.randint(4, const.CHAR_MID))).replace(' ', '')
    for name, c in categories.iteritems():
        category = Category.objects.create(name=name, n_min=c['n_min'], n_max=c['n_max'],
            v_step=c['v_step'], v_base=c['v_base'],
            free_time=c['free_time'], max_time=c['max_time']
        )
        c['id'] = category.id
        c['tags'] = []
        if name == 'empty':
            continue
        for i in range(0, 2):
            name = genName()
            while Tag.objects.filter(name=name).count() > 0:
                name = genName()
            tag = Tag.objects.create(name=name, category=category)
            t = {
                'name': tag.name,
                'cid': tag.category.id,
                'questions': [],
            }
            c['tags'].append(tag.id)
            if name == 'Programmer':
                for j in range(0, 10):
                    content = genName()
                    while Question.objects.filter(content=content).count() > 0:
                        content = genName()
                    question = Question.objects.create(content=content, level=random.randint(0, 5), tag=tag)
                    q = {
                        'content': question.content,
                        'tid': question.tag.id,
                        'level': question.level,
                        'op_ans': [],
                    }
                    t['questions'].append(question.id)
                    for k in range(0, 4):
                        content = genName()
                        while Question.objects.filter(content=content).count() > 0:
                            content = genName()
                        answer = OptionalAnswer.objects.create(
                            content=content, question=question, is_solution=(k == 0))
                        a = {
                            'content': answer.content,
                            'qid': answer.question.id,
                            'is_sln': answer.is_solution,
                        }
                        q['op_ans'].append(answer.id)
                        op_ans[answer.id] = a
                    questions[question.id] = q
            t['question_dist'] = tag.questionDistribution()
            tags[tag.id] = t
    cache.clear()
    self.categories = categories
    self.tags = tags
    self.questions = questions
    self.op_ans = op_ans


