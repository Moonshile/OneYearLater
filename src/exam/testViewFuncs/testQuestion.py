
from django.test import TestCase
from django.core.cache import cache
from django.core.urlresolvers import reverse

from exam import cc, ss
from exam.models import *
from exam.viewFuncs import *
from exam.views import *
from exam.tests import commonSetUp

class NextQuestionsWithRandomTagLevelTests(TestCase):

    def setUp(self):
        self.data = commonSetUp()
        self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.qids = self.client.session.get(ss.QUESTION_IDS, {})
        self.category = getCachedCategory(self.client.session[ss.CATEGORY_NAME])
        self.all_qid = map(
            lambda q: q['id'],
            reduce(
                lambda res, t: res + t['questions'],
                self.category['tags'],
                []
            )
        )

    """
    Generate next questions correctly when qids is empty
    """
    def test_next_questions_with_random_tag_level_empty_qids(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        actual = nextQuestionsWithRandomTagLevel(self.qids, self.category, count)
        self.assertEqual(len(actual), count)
        for q in actual:
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid, True)

    """
    Generate next questions correctly when qids is not empty
    """
    def test_next_questions_with_random_tag_level_nonempty_qids(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = random.sample(self.all_qid, len(self.all_qid)/2)
        actual = nextQuestionsWithRandomTagLevel(self.qids, self.category, count)
        self.assertEqual(len(actual), count)
        for q in actual:
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid, True)

    """
    Generate next questions correctly when there is not enough questions
    """
    def test_next_questions_with_random_tag_level_not_enough(self):
        count = len(self.all_qid)*2
        actual = nextQuestionsWithRandomTagLevel(self.qids, self.category, count)
        self.assertEqual(len(actual), len(self.all_qid))
        for q in actual:
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid, True)

    """
    Generate next questions correctly when there is no more questions
    """
    def test_next_questions_with_random_tag_level_no_more(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = self.all_qid
        actual = nextQuestionsWithRandomTagLevel(self.qids, self.category, count)
        self.assertEqual(len(actual), 0)

class NextQuestionsWithRandomTagTests(TestCase):

    def setUp(self):
        self.data = commonSetUp()
        self.level = 0
        self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.qids = self.client.session.get(ss.QUESTION_IDS, {})
        self.category = getCachedCategory(self.client.session[ss.CATEGORY_NAME])
        self.all_qid_with_level = map(
            lambda q: q['id'],
            filter(
                lambda q: q['level'] == self.level,
                reduce(
                    lambda res, t: res + t['questions'],
                    self.category['tags'],
                    []
                )
            )
        )
        self.all_qid = map(
            lambda q: q['id'],
            reduce(
                lambda res, t: res + t['questions'],
                self.category['tags'],
                []
            )
        )

    """
    Generate next questions correctly when qids is empty
    """
    def test_next_questions_with_random_tag_empty_qids(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        actual = nextQuestionsWithRandomTag(self.qids, self.category, self.level, count)
        self.assertEqual(len(actual), count)
        for q in actual:
            self.assertEqual(q['level'], self.level)
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid, True)

    """
    Generate next questions correctly when qids is not empty
    """
    def test_next_questions_with_random_tag_nonempty_qids(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = random.sample(self.all_qid, len(self.all_qid)/2)
        actual = nextQuestionsWithRandomTag(self.qids, self.category, self.level, count)
        self.assertEqual(len(actual), count)
        for q in actual:
            self.assertEqual(q['level'], self.level)
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid, True)

    """
    Generate next questions correctly when there is not enough questions
    """
    def test_next_questions_with_random_tag_not_enough(self):
        count = len(self.all_qid_with_level)*2
        actual = nextQuestionsWithRandomTag(self.qids, self.category, self.level, count)
        self.assertEqual(len(actual), len(self.all_qid_with_level))
        for q in actual:
            self.assertEqual(q['level'], self.level)
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid, True)

    """
    Generate next questions correctly when there is no more questions
    """
    def test_next_questions_with_random_tag_no_more(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = self.all_qid
        actual = nextQuestionsWithRandomTag(self.qids, self.category, self.level, count)
        self.assertEqual(len(actual), 0)

    """
    Generate next questions correctly when level is wrong
    """
    def test_next_questions_with_random_tag_wrong_level(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = self.all_qid
        actual = nextQuestionsWithRandomTag(self.qids, self.category, -1, count)
        self.assertEqual(len(actual), 0)

class NextQuestionsWithRandomLevelTests(TestCase):

    def setUp(self):
        self.data = commonSetUp()
        self.tag = self.data[0]['tags'][0]['name']
        self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.qids = self.client.session.get(ss.QUESTION_IDS, {})
        self.category = getCachedCategory(self.client.session[ss.CATEGORY_NAME])
        self.all_qid_with_tag = map(
            lambda q: q['id'],
            self.data[0]['tags'][0]['questions']
        )
        self.all_qid = map(
            lambda q: q['id'],
            reduce(
                lambda res, t: res + t['questions'],
                self.category['tags'],
                []
            )
        )

    """
    Generate next questions correctly when qids is empty
    """
    def test_next_questions_with_random_level_empty_qids(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        actual = nextQuestionsWithRandomLevel(self.qids, self.category, self.tag, count)
        self.assertEqual(len(actual), count)
        for q in actual:
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid_with_tag, True)

    """
    Generate next questions correctly when qids is not empty
    """
    def test_next_questions_with_random_level_nonempty_qids(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = random.sample(self.all_qid, len(self.all_qid)/2)
        actual = nextQuestionsWithRandomLevel(self.qids, self.category, self.tag, count)
        self.assertEqual(len(actual), count)
        for q in actual:
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid_with_tag, True)

    """
    Generate next questions correctly when there is not enough questions
    """
    def test_next_questions_with_random_level_not_enough(self):
        count = len(self.all_qid_with_tag)*2
        actual = nextQuestionsWithRandomLevel(self.qids, self.category, self.tag, count)
        self.assertEqual(len(actual), len(self.all_qid_with_tag))
        for q in actual:
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid_with_tag, True)

    """
    Generate next questions correctly when there is no more questions
    """
    def test_next_questions_with_random_level_no_more(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = self.all_qid
        actual = nextQuestionsWithRandomLevel(self.qids, self.category, self.tag, count)
        self.assertEqual(len(actual), 0)

    """
    Generate next questions correctly when tag is wrong
    """
    def test_next_questions_with_random_level_wrong_tag(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = self.all_qid
        actual = nextQuestionsWithRandomLevel(self.qids, self.category, 'not_exist', count)
        self.assertEqual(len(actual), 0)

class NextQuestionsWithFixedTagLevelTests(TestCase):

    def setUp(self):
        self.data = commonSetUp()
        self.tag = self.data[0]['tags'][0]['name']
        self.level = 0
        self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.qids = self.client.session.get(ss.QUESTION_IDS, {})
        self.category = getCachedCategory(self.client.session[ss.CATEGORY_NAME])
        self.all_qid_with_tag_level = map(
            lambda q: q['id'],
            filter(lambda q: q['level'] == self.level, self.data[0]['tags'][0]['questions'])
        )
        self.all_qid = map(
            lambda q: q['id'],
            reduce(
                lambda res, t: res + t['questions'],
                self.category['tags'],
                []
            )
        )

    """
    Generate next questions correctly when qids is empty
    """
    def test_next_questions_with_fixed_level_empty_qids(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        actual = nextQuestionsWithFixedTagLevel(self.qids, self.category, self.tag, self.level, count)
        self.assertEqual(len(actual), count)
        for q in actual:
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid_with_tag_level, True)

    """
    Generate next questions correctly when qids is not empty
    """
    def test_next_questions_with_fixed_level_nonempty_qids(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = random.sample(self.all_qid, len(self.all_qid_with_tag_level)/2)
        actual = nextQuestionsWithFixedTagLevel(self.qids, self.category, self.tag, self.level, count)
        self.assertEqual(len(actual), count)
        for q in actual:
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid_with_tag_level, True)

    """
    Generate next questions correctly when there is not enough questions
    """
    def test_next_questions_with_fixed_level_not_enough(self):
        count = len(self.all_qid_with_tag_level)*2
        actual = nextQuestionsWithFixedTagLevel(self.qids, self.category, self.tag, self.level, count)
        self.assertEqual(len(actual), len(self.all_qid_with_tag_level))
        for q in actual:
            self.assertEqual(q['id'] not in self.qids, True)
            self.assertEqual(q['id'] in self.all_qid_with_tag_level, True)

    """
    Generate next questions correctly when there is no more questions
    """
    def test_next_questions_with_fixed_level_no_more(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = self.all_qid
        actual = nextQuestionsWithFixedTagLevel(self.qids, self.category, self.tag, self.level, count)
        self.assertEqual(len(actual), 0)

    """
    Generate next questions correctly when tag is wrong
    """
    def test_next_questions_with_fixed_level_wrong_tag(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = self.all_qid
        actual = nextQuestionsWithFixedTagLevel(self.qids, self.category, 'not_exist', self.level, count)
        self.assertEqual(len(actual), 0)

    """
    Generate next questions correctly when level is wrong
    """
    def test_next_questions_with_fixed_level_wrong_level(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = self.all_qid
        actual = nextQuestionsWithFixedTagLevel(self.qids, self.category, self.tag, -1, count)
        self.assertEqual(len(actual), 0)

    """
    Generate next questions correctly when tag and level are wrong
    """
    def test_next_questions_with_fixed_level_wrong_tag_level(self):
        count = self.client.session[self.client.session[ss.Q_TOKEN]]
        self.qids = self.all_qid
        actual = nextQuestionsWithFixedTagLevel(self.qids, self.category, 'not_exist', -1, count)
        self.assertEqual(len(actual), 0)
