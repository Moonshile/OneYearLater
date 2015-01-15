
from django.test import TestCase

from exam.models import AnswerSheet, Category, Tag, Question
from exam.tests import commonSetUp

"""
Creates an answer sheet with no user and has a token generated
"""
def create_answer_sheet():
    answer_sheet = AnswerSheet.objects.create()
    answer_sheet.generateToken()
    return answer_sheet

class AnswerSheetMethodTest(TestCase):

    """
    token of an answer sheet should be long enough
    """
    def test_generate_token_enough_length(self):
        expect = 6
        actual = len(create_answer_sheet().token)
        self.assertEqual(actual >= expect, True)

    """
    token of an answer sheet shold not begin with '0x'
    """
    def test_generate_token_not_begin_with_0x(self):
        self.assertEqual(create_answer_sheet().token[0:2] == '0x', False)


class TagMethodTest(TestCase):

    def setUp(self):
        self.data = commonSetUp()

    """
    question_distribution should return a correct result
    """
    def test_question_distribution_correct(self):
        expect = {'l0': 2, 'l3': 1}
        actual = Tag.objects.get(name='C').questionDistribution()
        self.assertEqual(expect, actual)

