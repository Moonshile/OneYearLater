
from django.test import TestCase
from django.core.cache import cache
from django.core.urlresolvers import reverse

from exam import cc, ss
from exam.models import Category, Tag, Question, OptionalAnswer, Answer, AnswerSheet
from exam.viewFuncs import with_cache, getCachedCategories, getCachedOptionalAnswers, getCachedTags, getCachedQuestions
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

class GetCachedOptionalAnswersTests(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.data = commonSetUp(self)

    """
    Get answers correctly
    """
    def test_get_correctly(self):
        expect = self.op_ans
        actual = getCachedOptionalAnswers()
        self.assertEqual(actual, expect)

    """
    answers got are in cache
    """
    def test_in_cache(self):
        expect = getCachedOptionalAnswers()
        actual = cache.get(cc.OPTIONAL_ANS)
        self.assertEqual(actual, expect)

class GetCachedQuestionsTests(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.data = commonSetUp(self)

    """
    Get questions correctly
    """
    def test_get_correctly(self):
        expect = self.questions
        actual = getCachedQuestions()
        self.assertEqual(actual, expect)

    """
    questions got are in cache
    """
    def test_in_cache(self):
        expect = getCachedQuestions()
        actual = cache.get(cc.QUESTIONS)
        self.assertEqual(actual, expect)

class GetCachedTagsTests(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.data = commonSetUp(self)

    """
    Get questions correctly
    """
    def test_get_correctly(self):
        expect = self.tags
        actual = getCachedTags()
        self.assertEqual(actual, expect)

    """
    questions got are in cache
    """
    def test_in_cache(self):
        expect = getCachedTags()
        actual = cache.get(cc.TAGS)
        self.assertEqual(actual, expect)

class GetCachedCategoriesTests(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.data = commonSetUp(self)

    """
    Get questions correctly
    """
    def test_get_correctly(self):
        expect = self.categories
        actual = getCachedCategories()
        self.assertEqual(actual, expect)

    """
    questions got are in cache
    """
    def test_in_cache(self):
        expect = getCachedCategories()
        actual = cache.get(cc.CATEGORIES)
        self.assertEqual(actual, expect)



