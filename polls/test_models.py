# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from polls.models import Question, Choice

from datetime import date
from django.utils import timezone

class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        # create Question data
        Question.objects.create(
            question_text = 'this is the question?',
            pub_date = date(2018, 7, 20),
            slug = "old-slug"
        )

        Question.objects.create(
            question_text = 'this is another question?',
            pub_date = timezone.now(),
            slug = "new-slug"
        )

    def test_question_label(self):
        question = Question.objects.get(pk=1)
        field_label = question._meta.get_field('question_text').verbose_name
        self.assertEquals(field_label, 'question text')

    def test_question_length(self):
        question = Question.objects.get(pk=1)
        max_length = question._meta.get_field('question_text').max_length
        self.assertEquals(max_length, 200)

    def test_pub_date_label(self):
        question = Question.objects.get(pk=1)
        field_label = question._meta.get_field('pub_date').verbose_name
        self.assertEquals(field_label, 'date published')

    def test_was_published_recently_fails(self):
        question_old = Question.objects.get(pk=1)
        self.assertFalse(question_old.was_published_recently())

    def test_was_published_recently_passes(self):
        question_new = Question.objects.get(pk=2)
        self.assertTrue(question_new.was_published_recently())

    def test_question_str_name(self):
        question = Question.objects.get(pk=1)
        expected_object_name = question.question_text + "({})".format(question.slug)
        self.assertEquals(expected_object_name, str(question))

class ChoiceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        # create a dummy question
        Question.objects.create(
            question_text = 'this is the question?',
            pub_date = date(2018, 7, 20),
            slug = "q-slug"
        )

        # create Choice data
        Choice.objects.create(
            question = Question.objects.get(pk=1),
            choice_text = 'this is a choice.'
        )

    def test_question_label(self):
        choice = Choice.objects.get(pk=1)
        field_label = choice._meta.get_field('question').verbose_name
        self.assertEquals(field_label, 'question')

    def test_choice_text_label(self):
        choice = Choice.objects.get(pk=1)
        field_label = choice._meta.get_field('choice_text').verbose_name
        self.assertEquals(field_label, 'choice text')

    def test_choice_text_length(self):
        choice = Choice.objects.get(pk=1)
        max_length = choice._meta.get_field('choice_text').max_length
        self.assertEquals(max_length, 200)

    def test_votes_label(self):
        choice = Choice.objects.get(pk=1)
        field_label = choice._meta.get_field('votes').verbose_name
        self.assertEquals(field_label, 'votes')

    def test_votes_default_value(self):
        choice = Choice.objects.get(pk=1)
        expected_default_choice_value = 0
        self.assertEquals(expected_default_choice_value, choice.votes)

    def test_choice_str_name(self):
        choice = Choice.objects.get(pk=1)
        expected_object_name = choice.choice_text
        self.assertEquals(expected_object_name, str(choice))
