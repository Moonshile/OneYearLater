
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

class HandInAnswerTests(TestCase):

    def setUp(self):
        self.data = commonSetUp()
        self.category_name = self.data[0]['name']
        self.client.get(reverse(getTags), {'c': self.category_name})
        self.q_token = self.client.session[ss.Q_TOKEN]
        response = self.client.get(reverse(getQuestions), {'t': self.data[0]['tags'][0]['name'], 'q_token': self.q_token})
        self.questions = json.loads(response.content)['questions']
        self.op_ans = reduce(lambda res, q: res + q['op_ans'], self.questions, [])
        self.cached_op_ans = getCachedOptionalAnswers()

    """
    Hand in answer with wrong methods
    Should forbid
    """
    def test_hand_in_answer_with_wrong_methods(self):
        not_allowed = 405
        response = self.client.get(reverse(handInAnswer), {'id': 0, 'time': 10, 'q_token': self.q_token})
        self.assertEqual(response.status_code, not_allowed)
        response = self.client.delete(reverse(handInAnswer), {'id': 0, 'time': 10, 'q_token': self.q_token})
        self.assertEqual(response.status_code, not_allowed)
        response = self.client.head(reverse(handInAnswer), {'id': 0, 'time': 10, 'q_token': self.q_token})
        self.assertEqual(response.status_code, not_allowed)
        response = self.client.put(reverse(handInAnswer), {'id': 0, 'time': 10, 'q_token': self.q_token})
        self.assertEqual(response.status_code, not_allowed)
        response = self.client.patch(reverse(handInAnswer), {'id': 0, 'time': 10, 'q_token': self.q_token})
        self.assertEqual(response.status_code, not_allowed)

    """
    hand in answer with wrong answer id
    """
    def test_hand_in_answer_with_wrong_id(self):
        a = self.op_ans[0]
        q_token = self.client.session[ss.QUESTION_IDS][self.cached_op_ans[a['id']]['qid']][0]
        response = self.client.post(reverse(handInAnswer), {'id': -1, 'time': 10, 'q_token': q_token})
        actual = json.loads(response.content)
        self.assertEqual(actual['err_code'], err['ERROR'].code)
        self.assertEqual(set(actual['err_msg']), set(['id ' + err['ERROR'].msg, 'q_token ' + err['ERROR'].msg]))

    """
    hand in answer with wrong cost_time
    """
    def test_hand_in_answer_with_wrong_cost_time(self):
        a = self.op_ans[0]
        q_token = self.client.session[ss.QUESTION_IDS][self.cached_op_ans[a['id']]['qid']][0]
        response = self.client.post(reverse(handInAnswer), {'id': a['id'], 'time': -1, 'q_token': q_token})
        actual = json.loads(response.content)
        self.assertEqual(actual['err_code'], err['ERROR'].code)
        self.assertEqual(actual['err_msg'], ['time ' + err['ERROR'].msg])

    """
    hand in answer with wrong q_token
    """
    def test_hand_in_answer_with_wrong_q_token(self):
        a = self.op_ans[0]
        response = self.client.post(reverse(handInAnswer), {'id': a['id'], 'time': 10, 'q_token': 'not_exist'})
        actual = json.loads(response.content)
        self.assertEqual(actual['err_code'], err['ERROR'].code)
        self.assertEqual(actual['err_msg'], ['q_token ' + err['ERROR'].msg])

    """
    hand in answer correctly
    """
    def test_hand_in_answer_correctly(self):
        a = self.op_ans[0]
        q_token = self.client.session[ss.QUESTION_IDS][self.cached_op_ans[a['id']]['qid']][0]
        response = self.client.post(reverse(handInAnswer), {'id': a['id'], 'time': 10, 'q_token': q_token})
        actual = json.loads(response.content)
        self.assertEqual(actual['err_code'], err['OK'].code)
        self.assertEqual(actual['err_msg'], err['OK'].msg)
        self.assertEqual(a['id'] in map(lambda x: x['id'], self.client.session[ss.ANSWERS]), True)
