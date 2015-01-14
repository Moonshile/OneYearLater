
from django.test import TestCase

from exam.models import AnswerSheet, Category, Tag, Question

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
        category = Category.objects.create(name='Programmer')
        tagc = Tag.objects.create(name='C', category=category)
        tagc.question_set.add(Question(content='Is #include a macro?'))
        tagc.question_set.add(Question(content='Is main() necessary?'))
        tagc.question_set.add(Question(content='What does (*c)(const void *) means?', level=3))

    """
    question_distribution should return a correct result
    """
    def test_question_distribution_correct(self):
        expect = {0: 2, 3: 1}
        actual = Tag.objects.get(name='C').question_distribution()
        self.assertEqual(expect, actual)

