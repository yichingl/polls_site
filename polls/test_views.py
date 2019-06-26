# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from polls.models import Question, Choice

from datetime import date

class PollsIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass;

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/polls/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)

class PollsDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create Question data
        Question.objects.create(
            question_text = 'this is the question?',
            pub_date = date(2018, 7, 20)
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/polls/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        question = Question.objects.get(pk=1)
        response = self.client.get(reverse('polls:detail', kwargs={'question_pk': question.pk}))
        self.assertEqual(response.status_code, 200)

class PollsResultsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create Question data
        Question.objects.create(
            question_text = 'this is the question?',
            pub_date = date(2018, 7, 20)
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/polls/1/results/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        question = Question.objects.get(pk=1)
        response = self.client.get(reverse('polls:results', kwargs={'question_pk': question.pk}))
        self.assertEqual(response.status_code, 200)
