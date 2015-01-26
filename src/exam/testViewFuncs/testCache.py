
from django.test import TestCase
from django.core.cache import cache
from django.core.urlresolvers import reverse

from exam import cc, ss
from exam.models import *
from exam.viewFuncs import *
from exam.views import *
from exam.tests import commonSetUp

class WithCacheTests(TestCase):

    @with_cache("test_with_cache_decorator_func")
    def cacheData(self):
        self.value = 100
        return self.value

    def setUp(self):
        self.key = "test_with_cache_decorator_func"
        self.assertEqual(cache.get(self.key), None)
        self.cacheData()

    def tearDown(self):
        cache.clear()

    def test_with_cache_correct(self):
        actual = self.cacheData()
        self.assertEqual(actual, self.value)

    """
    the data is cached exactly
    """
    def test_with_cache_cached(self):
        actual = cache.get(self.key)
        self.assertEqual(actual, self.value)

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



