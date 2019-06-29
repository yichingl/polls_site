# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# to support Python 2
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

from datetime import timedelta
from django.utils import timezone


@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # additional field to track repeated questions from different sources
    slug = models.SlugField()

    def __str__(self):
        return self.question_text + "({})".format(self.slug)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timedelta(days=1)

@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
