
from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    owner = models.OneToOneField(User, primary_key=True)
    age = models.IntegerField(null=True)
    gender = models.NullBooleanField(null=True)

    def __unicode__(self):
        return self.owner.username + u'\'s account'

