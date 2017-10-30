
'''
Dummy models for testing django_troll
'''

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse

from django_troll.models import Comment

class Book(models.Model):
    comments = GenericRelation(Comment)

    def get_absolute_url(self):
        return reverse('book_detail', args=(self.pk,))

class Movie(models.Model):
    pass