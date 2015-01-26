
from django.test import TestCase
from django.core.cache import cache
from django.core.urlresolvers import reverse

from exam import cc, ss
from exam.models import *
from exam.viewFuncs import *
from exam.views import *
from exam.tests import commonSetUp

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

class ComputeScoreTests(TestCase):

    def setUp(self):
        self.data = commonSetUp()
        self.ans = []
        for i in range(0, 100):
            ans = []
            for i in range(0, 12):
                a = {}
                a['level'] = int(random.expovariate(3)*10)
                if a['level'] > 4:
                    a['level'] = int(random.expovariate(3)*10)
                a['time'] = random.randint(0, 10*a['level'])
                a['is_sln'] = True if random.randint(0, 5 + a['level']) in range(0, 3) else False
                ans.append(a)
            self.ans.append(ans)

    def test_compute_score(self):
        ans = self.ans
        for a in ans:
            score = computeScore(self.data[0], a)
            self.assertEqual(type(score), float)
        print_scores = False
        if print_scores:
            scores = map(lambda x: (int(10000*computeScore(self.data[0], x)))/10000, ans)
            print sorted(scores)
            print 'max', reduce(lambda res, x: x if x > res else res, scores, 0)
            print 'min', reduce(lambda res, x: x if x < res else res, scores, 1000)
            print 'mean', reduce(lambda res, x: res+x, scores, 0)/len(scores)

class ComputeRatioTests(TestCase):

    def test_compute_ratio(self):
        from forever.const import THETA_NUM
        for i in range(0, 100):
            total = random.randint(1, 1000) + THETA_NUM
            rank = random.randint(0, total + 1)
            self.assertEqual(computeRatio(rank, total, 0), rank/float(total))
        print_res = False
        if print_res:
            scores = range(0, 100)
            ratios = map(lambda x: int(100*computeRatio(0, 0, x)), scores)
            print ratios




