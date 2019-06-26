# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from polls.models import Question, Choice

from datetime import date

class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        # create Question data
        Question.objects.create(
            question_text = 'this is the question?',
            pub_date = date(2018, 7, 20)
        )

    def test_question_label(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('question_text').verbose_name
        self.assertEquals(field_label, 'question text')

    def test_question_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('question_text').max_length
        self.assertEquals(max_length, 200)

    def test_pub_date_label(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('pub_date').verbose_name
        self.assertEquals(field_label, 'date published')

class ChoiceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        # create a dummy question
        Question.objects.create(
            question_text = 'this is the question?',
            pub_date = date(2018, 7, 20)
        )

        # create Choice data
        Choice.objects.create(
            question = Question.objects.get(id=1),
            choice_text = 'this is a choice.'
        )

    def test_question_label(self):
        choice = Choice.objects.get(id=1)
        field_label = choice._meta.get_field('question').verbose_name
        self.assertEquals(field_label, 'question')

    def test_choice_text_label(self):
        choice = Choice.objects.get(id=1)
        field_label = choice._meta.get_field('choice_text').verbose_name
        self.assertEquals(field_label, 'choice text')

    def test_choice_text_length(self):
        choice = Choice.objects.get(id=1)
        max_length = hoice._meta.get_field('choice_text').max_length
        self.assertEquals(max_length, 200)

    def test_votes_label(self):
        choice = Choice.objects.get(id=1)
        field_label = choice._meta.get_field('votes').verbose_name
        self.assertEquals(field_label, 'votes')

    def test_votes_default_value(self):
        choice = Choice.objects.get(id=1)
        expected_default_choice_value = 0
        self.assertEquals(expected_default_choice_value, choice.votes)
