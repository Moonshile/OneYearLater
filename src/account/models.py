#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    """account infomation for users"""
    owner = models.OneToOneField(User, primary_key=True)
    avatar = models.ImageField(null=True)
    rank = models.IntegerField(null=False, default=0)

    def __unicode__(self):
        return self.owner.username + u'\'s account'

class InvitationCode(models.Model):
    """docstring for InvitationCode"""
    code = models.CharField(max_length=8)

    def __unicode__(self):
        return code
        

