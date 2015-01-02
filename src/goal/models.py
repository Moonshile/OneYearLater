
from django.db import models
from django.contrib.auth.models import User
import random

class Goal(models.Model):
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(protocol='IPv4', null=True)
    author = models.ForeignKey(User)
    no = models.PositiveIntegerField(default=0)

    def trick(self):
        return self.id + 2000 if self.id > 1000 else (self.id - 1)*3 + random.randrange(0, 3)

    class Meta:
        ordering = ['-time']

    def __unicode__(self):
        return self.author.username + '\'s goal: ' + self.content[0:10]

class ErrorInfo(models.Model):
    content = models.TextField()
