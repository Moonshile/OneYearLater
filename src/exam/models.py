
from django.db import models
from django.contrib.auth.models import User
import random

# classify tags to their categories, for example, 'Programmer', 'Gaokao'
class Category(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name

# classify the questions, for example, 'C', 'java', 'math', 'history'
class Tag(models.Model):
    category = models.ForeignKey(Category)
    name = models.TextField()

    def __unicode__(self):
        return self.name + 'in' + self.category.name

    """
    returns the distribution of each hard-level of questions in this tag
    """
    def question_distribution(self):
        dist = {}
        for q in self.question_set.all():
            if dist.has_key(q.level):
                dist[q.level] += 1
            else:
                dist[q.level] = 1
        return dist

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
    owner = models.ForeignKey(User, null=True)
    # associated with id, but visible to users
    # with this, users could get their report
    token = models.CharField(max_length=16)
    time = models.DateTimeField(auto_now_add=True)
    # skill experience of this user, smaller is inexperienced
    experience = models.SmallIntegerField(default=0)
    
    class Meta:
        ordering = ['-time']

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
    # level of cost time for answer this question, from 0 to 10 (s)
    cost_time = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return self.answer_sheet.owner.username + '\'s answer'

