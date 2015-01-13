from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    category = models.ForeignKey(Category)
    name = models.TextField()

    def __unicode__(self):
        return self.name + 'in' + self.category.name

class Question(models.Model):
    content = models.TextField()
    tag = models.ForeignKey(Tag)
    level = models.SmallIntegerField(default=0)
    solution = models.ForeignKey(OptionalAnswer)

class OptionalAnswer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question)

class AnswerSheet(models.Model):
    owner = models.ForeignKey(User)
    token = models.CharField(max_length=16)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-time']

    def __unicode__(self):
        return self.owner.username + '\'s answer sheet'

class Answer(models.Model):
    answerSheet = models.ForeignKey(AnswerSheet)
    choosedAnswer = models.ForeignKey(OptionalAnswer)
    costTime = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return self.answerSheet.owner.username + '\'s answer'

