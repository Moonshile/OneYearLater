
from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    content = models.TextField()
    time = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField(protocol='IPv4', null=True)
    author = models.ForeignKey(User)

    class Meta:
        ordering = ['-time']

    def __unicode__(self):
        return self.author.username + '\'s goal: ' + self.content[0:10]

