
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse

from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from exam.views import getTags, getQuestions, handInAnswer, finishAnswer
from forever.const import err

class GetTagsTests(TestCase):

    def setUp(self):
        self.data = [{
            'name': 'Programmer',
            'tags': [{
                'name': 'C', 
                'questions': [
                    {'content': 'Is #include a macro?', 'level': 0},
                    {'content': 'Is main() necessary?', 'level': 0},
                    {'content': 'What does (*c)(const void *) means?', 'level': 3},
                ]
            },]
        },]
        for c in self.data:
            category = Category.objects.create(name=c['name'])
            c['id'] = category.id
            for t in c['tags']:
                tag = Tag.objects.create(name=t['name'], category=category)
                t['id'] = tag.id
                for q in t['questions']:
                    question = Question.objects.create(content=q['content'], level=q['level'], tag=tag)
                    q['id'] = question.id

    """
    The request for get exist tags should return correct results
    """
    def test_get_tags_exist(self):
        for c in self.data:
            response = self.client.get(reverse(getTags), {'c': c['name']})
            expect = '''{
                "err_code": %d, 
                "err_msg": "%s", 
                "tags": [{"l0": 2, "l3": 1}], 
                "q_token": "%s"
            }''' % (err["OK"].code, err["OK"].msg, self.client.session['q_token'][-1])
            self.assertJSONEqual(response.content, expect)

    """
    The request for get tags in non-exist category
    """
    def test_get_tags_not_exist(self):
        not_exist_category = 'not_exist_category'
        response = self.client.get(reverse(getTags), {'c': not_exist_category})
        expect = '''{
            "err_code": %d,
            "err_msg": ["category %s"]
        }''' % (err["NOT_EXIST"].code, err["NOT_EXIST"].msg)
        self.assertJSONEqual(response.content, expect)

    """
    Requests too frequently
    """
    def test_get_tags_too_frequently(self):
        response = self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        for i in range(0, 10):
            response = self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.assertEqual(response.status_code, 403)





        
