
'''
Dummy models for testing django_troll
'''

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from django_troll.models import Comment

class Book(models.Model):
    comments = GenericRelation(Comment)

class Movie(models.Model):
    pass