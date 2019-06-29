
import unittest
import os
import datetime, pytz


from django.test import TestCase

from parse_data import read_url_data, parse_for_datetime
from parse_data import parse_for_states, parse_for_very_consv, parse_for_2
from parse_data import parse_for_pol_lean_groups, parse_ny_data, parse_pollster_data

from polls.models import Question, Choice


class ParseStrTestCase(unittest.TestCase):
    """ Tests for misc helper functions. """
    def setUp(self):

        # Online data
        url_online = 'https://bbotllc.github.io/candidate-interviews/political_leanings.json'
        self.online_text = read_url_data(url_online).read().replace("\r","").replace("\n","")

        # Local data
        rel_url = "parse_files/political_leanings_sample.json"
        abs_url = os.path.abspath(rel_url)
        url_local = "file://" + abs_url

        # Pollster data
        url_pollster = "https://elections.huffingtonpost.com/pollster/api/v2/charts.json"
        self.pollster_text = read_url_data(url_pollster).read().replace("\r","").replace("\n","")

        # Local pollster data
        rel_url = "parse_files/pollster_sample.json"
        abs_url = os.path.abspath(rel_url)
        url_local_pollster = "file://" + abs_url

        #  For checking text content
        response = read_url_data(url_local)
        self.local_text = response.read().replace("\r","").replace("\n","")

        # For checking other
        response = read_url_data(url_local)
        self.states_dict = parse_for_states(response)

        response = read_url_data(url_local)
        self.consv_dict = parse_for_very_consv(response)

        response = read_url_data(url_local)
        self.out_dict = parse_for_2(response)

        response = read_url_data(url_local)
        self.all_dict = parse_for_pol_lean_groups(response,
            ["Very conservative","Geography","N Size"])

    def tearDown(self):
        pass;

    def test_local_contents_read_correctly(self):
        expected_text_excerpt = '[ {   "Geography": '
        read_text_excerpt = self.local_text[0:len(expected_text_excerpt)]
        self.assertEqual(expected_text_excerpt, read_text_excerpt)

    def test_online_contents_read_correctly(self):
        expected_text_excerpt = '[ {   "Geography": '
        read_text_excerpt = self.online_text[0:len(expected_text_excerpt)]
        self.assertEqual(expected_text_excerpt, read_text_excerpt)

    def test_pollster_contents_read_correctly(self):
        expected_text_excerpt = '{"count":853,"cursor":"901"'
        read_text_excerpt = self.pollster_text[0:len(expected_text_excerpt)]
        self.assertEqual(expected_text_excerpt, read_text_excerpt)

    def test_parse_for_states(self):
        expected_states_dict = {0: {'Geography': 'California'},
        1: {'Geography': 'California'}, 2: {'Geography': 'New York'},
        3: {'Geography': 'New York'}, 4: {'Geography': 'Pennsylvania'}}
        self.assertEqual(expected_states_dict, self.states_dict)

    def test_parse_for_very_consv(self):
        expected_consv_dict = {
            0:{"Very conservative":0.06371055471},
            1:{"Very conservative":0.05999609205},
            2:{"Very conservative":0.05414788787},
            3:{"Very conservative":0.04865059808},
            4:{"Very conservative":0.08044835955}}
        self.assertEqual(expected_consv_dict, self.consv_dict)

    def test_parse_for_2(self):
        expected_out_dict = {
            0:{"Very conservative":0.06371055471, 'Geography': 'California'},
            1:{"Very conservative":0.05999609205, 'Geography': 'California'},
            2:{"Very conservative":0.05414788787, 'Geography': 'New York'},
            3:{"Very conservative":0.04865059808, 'Geography': 'New York'},
            4:{"Very conservative":0.08044835955, 'Geography': 'Pennsylvania'}}
        self.assertEqual(expected_out_dict, self.out_dict)

    def test_parse_for_pol_lean_groups(self):
        expected_out_dict = {
            0:{"Very conservative":0.06371055471, 'Geography': 'California',
                "N Size": "17,506"},
            1:{"Very conservative":0.05999609205, 'Geography': 'California',
                "N Size": "17,507"},
            2:{"Very conservative":0.05414788787, 'Geography': 'New York',
                "N Size": "11,710"},
            3:{"Very conservative":0.04865059808, 'Geography': 'New York',
                "N Size": "9,363"},
            4:{"Very conservative":0.08044835955, 'Geography': 'Pennsylvania',
                "N Size": "8,377"}}
        self.assertEqual(expected_out_dict, self.all_dict)

    def test_parse_for_datetime(self):
        str_datetime = "2009-07-30T09:23:08.000Z"
        expected_datetime = datetime.datetime(2009,07,30,9,23,8)
        self.assertEqual(expected_datetime, parse_for_datetime(str_datetime))

class ParsePoliticalLeanings(TestCase):
    """ Tests functions that extract and save data to database for Political
        Leanings using a small, local dataset. """

    @classmethod
    def setUpTestData(cls):
        rel_url = "parse_files/political_leanings_sample.json"
        abs_url = os.path.abspath(rel_url)
        local_political_leanings_url = "file://" + abs_url
        parse_ny_data(local_political_leanings_url)

    def test_political_leanings_question_added_to_database(self):
        question = Question.objects.get(pk=1)
        expected_question_text = 'What was your political leaning in 2011?'
        self.assertEqual(expected_question_text, question.question_text)

    def test_political_leanings_choice_added_to_database(self):
        question = Question.objects.get(pk=1)
        choice = Choice.objects.get(
            question = question,
            choice_text = "Moderate")
        expected_num_votes = 3779
        self.assertEqual(expected_num_votes, choice.votes)

class ParsePollster(TestCase):
    """ Tests functions that extract and save data to database for Pollster
        using a small, local dataset. """

    @classmethod
    def setUpTestData(cls):
        rel_url = "parse_files/pollster_sample.json"
        abs_url = os.path.abspath(rel_url)
        local_pollster_url = "file://" + abs_url

        parse_pollster_data(local_pollster_url)

    def test_pollster_question_added_to_database(self):
        question = Question.objects.get(pk=1)
        expected_question_text = "Do you approve or disapprove of the job Donald Trump is doing as president?"
        self.assertEqual(expected_question_text, question.question_text)

    def test_pollster_date_of_question_added_to_database(self):
        question = Question.objects.get(pk=1)
        expected_datetime = pytz.UTC.localize(datetime.datetime(2017, 1, 10, 23, 32, 55))
        self.assertEqual(expected_datetime, question.pub_date)

    def test_pollster_choice_added_to_database(self):
        question = Question.objects.get(pk=1)
        choice = Choice.objects.get(
            question = question,
            question__slug = "grinnell-selzer-28986",
            choice_text = "Disapprove"
            )
        expected_votes = 450
        self.assertEqual(expected_votes, choice.votes)


if __name__ == '__main__':
    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ParseStrTestCase)
    suite = unittest.TestLoader().loadTestsFromTestCase(ParsePoliticalLeanings)
    suite = unittest.TestLoader().loadTestsFromTestCase(ParsePollster)
