# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from polls.models import Question, Choice

from django.utils import timezone

class QuestionsIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        # create set of Questions with known pub_dates
        num_questions = 8
        for q_pk in range(1,num_questions+1):
            Question.objects.create(
                question_text = 'Q?' + str(q_pk),
                pub_date = timezone.now()
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/polls/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_displays_5_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertTrue(len(response.context['latest_question_list']), 5)

    def test_index_questions_ordered_by_pub_date(self):
        response = self.client.get(reverse('polls:index'))
        latest_question_list = response.context['latest_question_list']
        self.assertGreater(latest_question_list[0].pub_date, latest_question_list[4].pub_date)

class QuestionDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create Question data
        Question.objects.create(
            question_text = 'this is the question?',
            pub_date = timezone.now()
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/polls/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        question = Question.objects.get(pk=1)
        response = self.client.get(reverse('polls:detail', kwargs={'question_pk': question.pk}))
        self.assertEqual(response.status_code, 200)

    def test_gets_correct_existing_object(self):
        question = Question.objects.get(pk=1)
        response = self.client.get(reverse('polls:detail', kwargs={'question_pk': question.pk}))
        returned_question = response.context['question']
        self.assertEqual(question, returned_question)

    def test_returns_404_nonexisting_object(self):
        response = self.client.get(reverse('polls:detail', kwargs={'question_pk': 30}))
        self.assertEqual(response.status_code, 404)


class QuestionResultsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create Question data
        Question.objects.create(
            question_text = 'this is the question?',
            pub_date = timezone.now()
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/polls/1/results/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        question = Question.objects.get(pk=1)
        response = self.client.get(reverse('polls:results', kwargs={'question_pk': question.pk}))
        self.assertEqual(response.status_code, 200)

class QuestionVoteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create Question data
        Question.objects.create(
            question_text = 'this is the question?',
            pub_date = timezone.now()
        )

        # create Choice data
        question = Question.objects.get(pk=1)
        Choice.objects.create(
            question = question,
            choice_text = 'choice 1',
        )
        Choice.objects.create(
            question = question,
            choice_text = 'choice 2',
        )
        Choice.objects.create(
            question = question,
            choice_text = 'choice 3',
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/polls/1/vote/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        question = Question.objects.get(pk=1)
        response = self.client.get(reverse('polls:vote', kwargs={'question_pk': question.pk}))
        self.assertEqual(response.status_code, 200)
