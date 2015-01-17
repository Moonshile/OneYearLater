
from django.test import TestCase
from django.core.cache import cache

from exam.models import *
from exam.viewFuncs import *
from exam.tests import commonSetUp

class GetQuestionsInTagTests(TestCase):

    def setUp(self):
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
        tag = Tag.objects.filter(name='C++')[0]
        expect = []
        actual = getQuestionsInTag(tag)
        self.assertEqual(actual, expect)

class GetTagsInCategoryTests(TestCase):

    def setUp(self):
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
        for c in self.data:
            cache.delete('category' + c['name'])

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
            actual = cache.get('category' + c['name'])
            self.assertEqual(actual, expect)

class GetCachedTagCategoryMapTests(TestCase):

    def setUp(self):
        self.cache_key = 'tag_category_map'
        cache.delete(self.cache_key)
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
        actual = cache.get(self.cache_key)
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

