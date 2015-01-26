
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.http import JsonResponse
import json

from exam import ss
from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from exam.views import *
from exam.viewFuncs import *
from exam.tests import commonSetUp
from forever.const import err, REQ_FREQUENCY_LIMIT

class FinishAnswerTests(TestCase):

    def setUp(self):
        self.data = commonSetUp()
        self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        q_token = self.client.session[ss.Q_TOKEN]
        session = self.client.session
        session[q_token] = 20
        session.save()
        response = self.client.get(reverse(getQuestions), {'q_token': q_token})
        response_data = json.loads(response.content)
        self.q_token = self.client.session[ss.Q_TOKEN]
        self.assertEqual(len(response_data['questions']), 20)
        self.assertEqual(self.client.session[self.q_token], 0)
        self.choosed_ans = map(lambda q: { 
            'id': q['op_ans'][0]['id'],
            'time': random.randint(0, 100), 
            'q_token': response_data['q_token']
        }, filter(lambda q: len(q['op_ans']) > 0, response_data['questions']))
        for a in self.choosed_ans:
            self.client.post(reverse(handInAnswer), a)

    """
    finish with wrong methods
    Should not allow
    """
    def test_finish_answer_with_wrong_methods(self):
        not_allowed = 405
        response = self.client.get(reverse(finishAnswer), {'q_token': self.q_token})
        self.assertEqual(response.status_code, not_allowed)
        response = self.client.delete(reverse(finishAnswer), {'id': 0, 'time': 10, 'q_token': self.q_token})
        self.assertEqual(response.status_code, not_allowed)
        response = self.client.head(reverse(finishAnswer), {'q_token': self.q_token})
        self.assertEqual(response.status_code, not_allowed)
        response = self.client.put(reverse(finishAnswer), {'time': 10, 'q_token': self.q_token})
        self.assertEqual(response.status_code, not_allowed)
        response = self.client.patch(reverse(finishAnswer), {'id': 0, 'time': 10, 'q_token': self.q_token})
        self.assertEqual(response.status_code, not_allowed)

    """
    finish with correct q_token
    """
    def test_finish_answer_correctly(self):
        response = self.client.post(reverse(finishAnswer), {'q_token': self.q_token})
        actual = json.loads(response.content)
        for a in self.choosed_ans:
            self.assertEqual(Answer.objects.filter(choosed_answer_id=a['id']).count() > 0, True)
        self.assertEqual(actual['err_code'], err['OK'].code)

    """
    finish with wrong q_token
    Should not allow
    """
    def test_finish_answer_with_wrong_q_token(self):
        forbidden = 403
        response = self.client.post(reverse(finishAnswer), {'q_token': 'not_exist'})
        self.assertEqual(response.status_code, forbidden)



