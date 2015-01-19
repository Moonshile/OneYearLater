
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.http import JsonResponse
import json

from exam import ss
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
            }''' % (err['OK'].code, err['OK'].msg, expect_tags, self.client.session[ss.Q_TOKEN])
            self.assertJSONEqual(response.content, expect)
            self.assertEqual(self.client.session[self.client.session[ss.Q_TOKEN]], c['n_first_batch'])
            self.assertEqual(self.client.session[ss.CATEGORY_NAME], c['name'])

    """
    The request for get tags in non-exist category
    """
    def test_get_tags_not_exist(self):
        not_exist_category = 'not_exist_category'
        response = self.client.get(reverse(getTags), {'c': not_exist_category})
        expect = '''{
            "err_code": %d,
            "err_msg": ["category %s"]
        }''' % (err['NOT_EXIST'].code, err['NOT_EXIST'].msg)
        self.assertJSONEqual(response.content, expect)

    """
    Requests too frequently
    """
    def test_get_tags_too_frequently(self):
        response = self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        forbid_code = 403
        for i in range(0, REQ_FREQUENCY_LIMIT + 1):
            # within the permitted count, get normal response
            self.assertEqual(response.status_code, 200)
            response = self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        # access frequency is over the limitation, then forbid
        self.assertEqual(response.status_code, forbid_code)
        import time
        # during the forbidden-time, access will refresh the forbidden-time
        time.sleep(1) # sleep 1 second
        response = self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.assertEqual(response.status_code, forbid_code)
        # forbidden-time has been refreshed by the lastest access
        time.sleep(1.5)
        response = self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.assertEqual(response.status_code, forbid_code)
        # now could access normally again
        time.sleep(2.5)
        response = self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.assertEqual(response.status_code, 200)

class GetQuestionsTests(TestCase):

    def setUp(self):
        self.data = commonSetUp()
        self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.client.session.clear()

    def assertCommon(self, actual_dict, expect_err_str, tag=None, level=None):
        expect_err = err[expect_err_str]
        actual = actual_dict
        expect_q_token = self.client.session[ss.Q_TOKEN]
        expect_has_next = True if self.client.session[expect_q_token] else False
        self.assertEqual(actual['err_code'], expect_err.code)
        self.assertEqual(actual['err_msg'], expect_err.msg)
        self.assertEqual(actual['q_token'], expect_q_token)
        self.assertEqual(actual['has_next'], expect_has_next)
        # no duplicated questions
        qs = []
        for q in actual['questions']:
            self.assertEqual(q['id'] not in qs, True)
            qs.append(q['id'])
        # the actual questions are correct
        for q in actual['questions']:
            if level:
                self.assertEqual(q['level'], expect_level)
            q_in_questions = reduce(
                lambda res, t: res or q in t['questions'],
                filter(
                    lambda t: not tag or t['name'] == tag,
                    self.data[0]['tags']
                ),
                False
            )
            self.assertEqual(q_in_questions, True)

    def hackSession(self, key, value):
        session = self.client.session
        session[key] = value
        session.save()

    """
    Get questions with random tag and random level correctly
    """
    def test_get_questions_random_tag_level(self):
        q_token = self.client.session[ss.Q_TOKEN]
        # the first loop for initial questions, and others for next questions
        for i in range(0, 3):
            expect_count = self.client.session[self.client.session[ss.Q_TOKEN]]
            response = self.client.get(reverse(getQuestions), {'q_token': q_token})
            actual = json.loads(response.content)
            self.assertCommon(actual_dict=actual, expect_err_str='OK')
            q_token = self.client.session[ss.Q_TOKEN]

    """
    Get questions with random tag correctly
    """
    def test_get_questions_random_tag(self):
        expect_level = 0
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        # the first loop for initial questions, and others for next questions
        for i in range(0, 3):
            expect_count = self.client.session[self.client.session[ss.Q_TOKEN]]
            response = self.client.get(reverse(getQuestions), {'l': expect_level, 'q_token': q_token})
            actual = json.loads(response.content)
            self.assertCommon(actual_dict=actual, expect_err_str='OK', level=expect_level)
            q_token = self.client.session[ss.Q_TOKEN]

    """
    Get questions with random level correctly
    """
    def test_get_questions_random_level(self):
        expect_tag = 'C'
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        # the first loop for initial questions, and others for next questions
        for i in range(0, 3):
            expect_count = self.client.session[self.client.session[ss.Q_TOKEN]]
            response = self.client.get(reverse(getQuestions), {'t': expect_tag, 'q_token': q_token})
            actual = json.loads(response.content)
            self.assertCommon(actual_dict=actual, expect_err_str='OK', tag=expect_tag)
            q_token = self.client.session[ss.Q_TOKEN]

    """
    Get questions with fixed tag and level correctly
    """
    def test_get_questions_fixed_tag_level(self):
        expect_level = 0
        expect_tag = 'C'
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        # the first loop for initial questions, and others for next questions
        for i in range(0, 3):
            expect_count = self.client.session[self.client.session[ss.Q_TOKEN]]
            response = self.client.get(reverse(getQuestions), {'t': expect_tag, 'l': expect_level, 'q_token': q_token})
            actual = json.loads(response.content)
            self.assertCommon(actual_dict=actual, expect_err_str='OK', tag=expect_tag, level=expect_level)
            q_token = self.client.session[ss.Q_TOKEN]

    """
    Get questions without reduplicated ones
    """
    def test_get_questions_without_dup(self):
        # this feature has been asserted in the above tests
        pass
    
    """
    Get initial questions with wrong tag
    should get a empty quesion list
    """
    def test_get_initial_questions_with_wrong_tag(self):
        wrong_tag = 'not_exist'
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        # assert
        response = self.client.get(reverse(getQuestions), {'t': wrong_tag, 'q_token': q_token})
        actual = json.loads(response.content)
        self.assertEqual(actual['questions'], [])

    """
    Get next questions with wrong tag
    should get a empty quesion list
    """
    def test_get_next_questions_with_wrong_tag(self):
        wrong_tag = 'not_exist'
        exist_tag = self.data[0]['tags'][0]['name']
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        response = self.client.get(reverse(getQuestions), {'t': exist_tag, 'q_token': q_token})
        q_token = self.client.session[ss.Q_TOKEN]
        # assert
        response = self.client.get(reverse(getQuestions), {'t': wrong_tag, 'q_token': q_token})
        actual = json.loads(response.content)
        self.assertEqual(actual['questions'], [])

    """
    Get initial questions with wrong level
    should get a empty quesion list
    """
    def test_get_initial_questions_with_wrong_level(self):
        wrong_level = -1
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        # assert
        response = self.client.get(reverse(getQuestions), {'l': wrong_level, 'q_token': q_token})
        actual = json.loads(response.content)
        self.assertEqual(actual['questions'], [])

    """
    Get next questions with wrong level
    should get a empty quesion list
    """
    def test_get_next_questions_with_wrong_level(self):
        wrong_level = -1
        exist_level = 0
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        response = self.client.get(reverse(getQuestions), {'l': exist_level, 'q_token': q_token})
        q_token = self.client.session[ss.Q_TOKEN]
        # assert
        response = self.client.get(reverse(getQuestions), {'l': wrong_level, 'q_token': q_token})
        actual = json.loads(response.content)
        self.assertEqual(actual['questions'], [])

    """
    Still has but not enough questions
    Should return all the rest questions and set bound value to q_token to 0
    """
    def test_get_questions_has_but_not_enough(self):
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        # hack the count of questions requested so that there is not enough questions
        expect_count = reduce(lambda res, t: res + len(t['questions']), self.data[0]['tags'], 0)
        self.hackSession(q_token, expect_count + 1)
        # assert
        response = self.client.get(reverse(getQuestions), {'q_token': q_token})
        actual = json.loads(response.content)
        self.assertCommon(actual_dict=actual, expect_err_str='OK')
        self.assertEqual(len(actual['questions']), expect_count)
        q_token = self.client.session[ss.Q_TOKEN]
        self.assertEqual(self.client.session[q_token], 0)

    """
    Has no new questions
    Should return empty question list and set bound value to q_token to 0
    """
    def test_get_questions_but_no_more(self):
        not_found = 404
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        # hack the count of questions requested so that there is not enough questions
        self.hackSession(q_token, reduce(lambda res, t: res + len(t['questions']), self.data[0]['tags'], 0))
        response = self.client.get(reverse(getQuestions), {'q_token': q_token})
        q_token = self.client.session[ss.Q_TOKEN]
        self.assertEqual(self.client.session[q_token], 0)
        # assert
        response = self.client.get(reverse(getQuestions), {'q_token': q_token})
        self.assertEqual(response.status_code, not_found)


    """
    Get questions with wrong q_token
    should forbid
    """
    def test_get_questions_with_wrong_q_token(self):
        tag = self.data[0]['tags'][0]['name']
        level = 0
        forbidden_code = 403
        # preparation
        q_token = 'wrong'
        # assert
        response = self.client.get(reverse(getQuestions), {'t': tag, 'l': level, 'q_token': q_token})
        self.assertEqual(response.status_code, forbidden_code)

    """
    Get last question with enough correct answers
    After this get, the bound value to q_token should be set to 0
    """
    def test_get_last_question_with_enough_correct(self):
        tag = self.data[0]['tags'][0]['name']
        level = 0
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        response = self.client.get(reverse(getQuestions), {'l': level, 't': tag, 'q_token': q_token})
        q_token = self.client.session[ss.Q_TOKEN]
        # hack the handed-in answers in session
        ans = OptionalAnswer.objects.filter(is_solution=True)[0].id
        ans_session = []
        for i in range(0, self.data[0]['n_min']):
            ans_session.append(ans)
        self.hackSession(ss.ANSWERS, ans_session)
        # assert
        response = self.client.get(reverse(getQuestions), {'l': level, 't': tag, 'q_token': q_token})
        actual = json.loads(response.content)
        q_token = self.client.session[ss.Q_TOKEN]
        self.assertEqual(self.client.session[q_token], 0)
        self.assertCommon(actual_dict=actual, expect_err_str='OK', tag=tag, level=level)

    """
    Get last question with having answered max number of questions
    Bound value to q_token should be set to 0
    """
    def test_get_last_question_with_answered_max(self):
        tag = self.data[0]['tags'][0]['name']
        level = 0
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        response = self.client.get(reverse(getQuestions), {'l': level, 't': tag, 'q_token': q_token})
        q_token = self.client.session[ss.Q_TOKEN]
        # hack the total qids in session
        qids_session = {}
        for i in range(0, self.data[0]['n_max']):
            qids_session[i] = q_token
        self.hackSession(ss.QUESTION_IDS, qids_session)
        # assert
        response = self.client.get(reverse(getQuestions), {'l': level, 't': tag, 'q_token': q_token})
        actual = json.loads(response.content)
        q_token = self.client.session[ss.Q_TOKEN]
        self.assertEqual(self.client.session[q_token], 0)
        self.assertCommon(actual_dict=actual, expect_err_str='OK', tag=tag, level=level)

    """
    Get questions with q_token bound with 0
    Should return 404
    """
    def test_get_questions_with_q_token_bound_0(self):
        tag = self.data[0]['tags'][0]['name']
        level = 0
        not_found_code = 404
        # preparation
        q_token = self.client.session[ss.Q_TOKEN]
        response = self.client.get(reverse(getQuestions), {'l': level, 't': tag, 'q_token': q_token})
        q_token = self.client.session[ss.Q_TOKEN]
        # hack the bound value to q_token
        self.hackSession(q_token, 0)
        # assert
        response = self.client.get(reverse(getQuestions), {'l': level, 't': tag, 'q_token': q_token})
        self.assertEqual(response.status_code, not_found_code)

class HandInAnswerTests(TestCase):

    def setUp(self):
        self.data = commonSetUp()
        self.category_name = self.data[0]['name']
        self.client.get(reverse(getTags), {'c': self.category_name})
        q_token = self.client.session[ss.Q_TOKEN]

    """
    hand in answer with wrong answer id
    """
    def test_hand_in_answer_with_wrong_id(self):
        pass

    """
    hand in answer with wrong cost_time
    """
    def test_hand_in_answer_with_wrong_cost_time(self):
        pass

    """
    hand in answer with wrong q_token
    """
    def test_hand_in_answer_with_wrong_q_token(self):
        pass

    """
    hand in answer correctly
    """
    def test_hand_in_answer_correctly(self):
        pass


