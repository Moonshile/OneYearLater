#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    owner = models.ForeignKey(User, null=False)
    text = models.CharField(max_length=20, unique=True)

class Dessert(models.Model):
    activity = models.ForeignKey(Activity, null=False)
    description = models.TextField()
    photo = models.ImageField()
