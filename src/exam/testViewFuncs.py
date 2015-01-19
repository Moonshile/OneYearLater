
from django.test import TestCase
from django.core.cache import cache
from django.core.urlresolvers import reverse

from exam import cc, ss
from exam.models import *
from exam.viewFuncs import *
from exam.views import *
from exam.tests import commonSetUp

class GetOptionalAnswersOfQuestionTests(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.data = commonSetUp()

    """
    Get answers of a question with many answers
    """
    def test_get_many_answers_of_question(self):
        q = OptionalAnswer.objects.all()[0].question
        expect = self.data[0]['tags'][0]['questions'][0]['op_ans']
        actual = getOptionalAnswersOfQuestion(q)
        self.assertEqual(actual, expect)

    """
    Get answers of a question with no answer
    """
    def test_get_no_question_in_tag(self):
        q = filter(lambda x: x.optionalanswer_set.count() == 0, Question.objects.all())[0]
        expect = []
        actual = getOptionalAnswersOfQuestion(q)
        self.assertEqual(actual, expect)

class GetQuestionsInTagTests(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.data = commonSetUp()

    """
    Get questions in an tag with many questions
    """
    def test_get_many_questions_in_tag(self):
        tag = Tag.objects.filter(name='C')[0]
        expect = self.data[0]['tags'][0]['questions']
        actual = getQuestionsInTag(tag)
        self.assertEqual(actual, expect)

    """
    Get questions in an tag with no question
    """
    def test_get_no_question_in_tag(self):
        tag = Tag.objects.filter(name='Empty')[0]
        expect = []
        actual = getQuestionsInTag(tag)
        self.assertEqual(actual, expect)

class GetTagsInCategoryTests(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.data = commonSetUp()

    """
    Get tags in a category with many tags
    """
    def test_get_many_tags_in_category(self):
        c = Category.objects.filter(name='Programmer')[0]
        expect = self.data[0]['tags']
        actual = getTagsInCategory(c)
        self.assertEqual(actual, expect)

    """
    Get tags in a category with no tag
    """
    def test_get_no_tag_in_category(self):
        c = Category.objects.filter(name='Gaokao')[0]
        expect = []
        actual = getTagsInCategory(c)
        self.assertEqual(actual, expect)

class GetCachedCategoryTests(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.data = commonSetUp()
        cache.clear()

    """
    Get data of exist category
    """
    def test_data_of_get_cached_category(self):
        for c in self.data:
            expect = c
            actual = getCachedCategory(c['name'])
            self.assertEqual(actual, expect)

    """
    Get data of not exist category
    """
    def test_data_of_get_not_exist_category(self):
        expect = None
        actual = getCachedCategory('not_exist')
        self.assertEqual(actual, expect)

    """
    Assert cache of category
    """
    def test_cached_data_of_get_cached_category(self):
        for c in self.data:
            expect = getCachedCategory(c['name'])
            actual = cache.get(cc.CATEGORY_BASE + c['name'])
            self.assertEqual(actual, expect)

class GetCachedTagCategoryMapTests(TestCase):

    def setUp(self):
        cache.clear()
        self.data = commonSetUp()

    """
    Get correct tag category map
    """
    def test_get_correct_cached_tag_category_map(self):
        tags = getCachedTagCategoryMap()
        for c in self.data:
            expect = c['name']
            for t in c['tags']:
                actual = tags[t['name']]
                self.assertEqual(actual, expect)

    """
    The map is in cached
    """
    def test_got_tag_category_map_is_in_cache(self):
        expect = getCachedTagCategoryMap()
        actual = cache.get(cc.TAG_CATEGORY_MAP)
        self.assertEqual(actual, expect)

class GenQtokenTests(TestCase):

    """
    Generate a string
    """
    def test_generate_string_q_token(self):
        expect = '<type \'str\'>'
        actual = str(type(genQtoken()))
        self.assertEqual(actual, expect)

    """
    Generate a 6-character string
    """
    def test_generate_6_char_q_token(self):
        import re
        pattern = re.compile(r'[A-Z0-9]{6}')
        for i in range(0, 100):
            actual = True if pattern.match(genQtoken()) else False
            self.assertEqual(actual, True)

class NextQuestionsWithRandomTagLevelTests(TestCase):

    def setUp(self):
        self.data = commonSetUp()
        self.client.get(reverse(getTags), {'c': self.data[0]['name']})
        self.qids = self.client.session.get(ss.QUESTION_IDS, [])
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
        self.qids = self.client.session.get(ss.QUESTION_IDS, [])
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
        self.qids = self.client.session.get(ss.QUESTION_IDS, [])
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
        self.qids = self.client.session.get(ss.QUESTION_IDS, [])
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





