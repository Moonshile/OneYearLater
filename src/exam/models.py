
from django.db import models
from django.contrib.auth.models import User
import random

from forever import const

# classify tags to their categories, for example, 'Programmer', 'Gaokao'
class Category(models.Model):
    name = models.CharField(max_length=const.CHAR_MID, unique=True)
    # count of questions should be requested the first time
    n_first_batch = models.SmallIntegerField(default=5)
    # count of questions should be requested the subsequent times
    n_next_batch = models.SmallIntegerField(default=1)
    # if user has answered this number of questions correctly, then finish
    n_min = models.SmallIntegerField(default=10)
    # else if user has answered this number of questions totally, then finish
    n_max = models.SmallIntegerField(default=15)
    # value of a questions is level*v_step + v_base
    v_step = models.SmallIntegerField(default=0)
    v_base = models.SmallIntegerField(default=0)
    # free time is the time for user to prepare and understand a question
    free_time = models.SmallIntegerField(default=0)
    # if a question cost time more than max_time, then treat it as max_time
    max_time = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return self.name

# classify the questions, for example, 'C', 'java', 'math', 'history'
class Tag(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=const.CHAR_MID, unique=True)

    def __unicode__(self):
        return self.name + 'in' + self.category.name

    """
    returns the distribution of each hard-level of questions in this tag
    """
    def questionDistribution(self):
        dist = {}
        for q in self.question_set.all():
            key = q.level
            if dist.has_key(key):
                dist[key] += 1
            else:
                dist[key] = 1
        res = []
        for k in dist:
            res.append({'level': k, 'count': dist[k]})
        return res

# only choice questions
class Question(models.Model):
    content = models.TextField()
    tag = models.ForeignKey(Tag)
    # level measures how hard the question is, smaller is easier
    level = models.SmallIntegerField(default=0)

# choices of questions
class OptionalAnswer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question)
    # is solution to the associated question or not
    is_solution = models.BooleanField(default=False)

# a user could attend exam again and again
class AnswerSheet(models.Model):
    owner = models.ForeignKey(User, null=True, default=None)
    # associated with id, but visible to users
    # with this, users could get their report
    token = models.CharField(max_length=8, unique=True)
    time = models.DateTimeField(auto_now_add=True)
    # score, is read only, so could be saved into db
    score = models.PositiveIntegerField(default=0, db_index=True)
    
    def generateToken(self):
        self.token = hex(self.id + 10000000)[2:]
        self.save()
        return self.token

    def __unicode__(self):
        return self.owner.username + '\'s answer sheet'

# actual answers in answer sheets
class Answer(models.Model):
    answer_sheet = models.ForeignKey(AnswerSheet)
    choosed_answer = models.ForeignKey(OptionalAnswer)
    # level of cost time for answer this question
    cost_time = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return self.answer_sheet.owner.username + '\'s answer'

