
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from exam.views import getTags, getQuestions, handInAnswer, finishAnswer
from exam.tests import commonSetUp
from forever.const import err, REQ_FREQUENCY_LIMIT

class GetTagsTests(TestCase):

    def setUp(self):
        self.data = commonSetUp()

    """
    The request for get exist tags should return correct results
    """
    def test_get_tags_exist(self):
        for c in self.data:
            response = self.client.get(reverse(getTags), {'c': c['name']})
            expect_tags = str(map(lambda t: {
                'name': t['name'], 
                'question_dist': t['question_dist']
            }, c['tags'])).replace('\'', '\"')
            expect = '''{
                "err_code": %d, 
                "err_msg": "%s", 
                "tags": %s, 
                "q_token": "%s"
            }''' % (err["OK"].code, err["OK"].msg, expect_tags, self.client.session['q_token'])
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
        for i in range(0, REQ_FREQUENCY_LIMIT + 1):
            self.assertEqual(response.status_code, 200)
            response = self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.assertEqual(response.status_code, 403)
        import time
        time.sleep(1) # sleep 1 second
        response = self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.assertEqual(response.status_code, 403)
        time.sleep(2.5)
        response = self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.assertEqual(response.status_code, 200)





        
