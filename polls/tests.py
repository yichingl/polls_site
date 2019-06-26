# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

class PollsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass;

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/polls/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
