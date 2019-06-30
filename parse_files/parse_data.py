import urllib2
import os
import re
import json

import datetime
from django.utils import timezone

from polls.models import Question, Choice

def parse_for_datetime(dstr):
    """ Given a pollster datetime str, return a datetime object. """
    return datetime.datetime.strptime(dstr, "%Y-%m-%dT%H:%M:%S.000Z")

def read_url_data(url):
    """ Reads data at given url and returns response object. """
    try:
        response = urllib2.urlopen(url)
        return response
    except urllib2.URLError as e:
        print(e.reason)
    except urllib2.HTTPError as e:
        print(e.code)
        print(e.read())

def parse_for_states(response):
    """ Parses given response object and returns a dict containing
        entry# and state as key-value pairs. """

    data = json.loads(response.read())

    name = "Geography"

    states_dict = {}
    for cnt, entry in enumerate(data):
        states_dict[cnt] = {name:entry[name]}

    return states_dict

def parse_for_very_consv(response):
    """ Parses given response object and returns a dict containing
        entry# and state as key-value pairs. """

    data = json.loads(response.read())

    name = "Very conservative"

    consv_dict = {}
    for cnt, entry in enumerate(data):
        consv_dict[cnt] = {name:entry[name]}

    return consv_dict

def parse_for_2(response):
    """ Parses given response object and returns a dict containing
        entry# and state,consv as key-value pairs. """

    group0 = "Very conservative"

    group1 = "Geography"

    data = json.loads(response.read())

    out_dict = {}
    for cnt, entry in enumerate(data):
        out_dict[cnt] = {}
        out_dict[cnt][group0] = entry[group0]
        out_dict[cnt][group1] = entry[group1]

    return out_dict

def parse_for_pol_lean_groups(response, list_of_groups):
    """ Parses given response object and returns a dict containing
        entry# and group data as key-value pairs. """

    data = json.loads(response.read())

    out_dict = {}
    for cnt, entry in enumerate(data):
        out_dict[cnt] = {}
        for group in list_of_groups:
            out_dict[cnt][group] = entry[group]

    return out_dict

def parse_ny_data(url):
    """ Extracts data from input political_leanings url to
        populate Question/Choice models in database. """

    # read data from input url
    response = read_url_data(url)
    data = json.loads(response.read())

    # choices to parse for
    choices = ["Very conservative","Conservative, (or)",
        "Moderate","Liberal, (or)", "Very liberal"]

    for entry in data:
        # only save data for New York polls
        if entry["Geography"] == "New York":
            # add entry to database
            question = Question.objects.get_or_create(
                question_text = 'What was your political leaning in {}?'.format(entry["Time"]) ,
                pub_date = datetime.date(entry["Time"],1,1),
                slug = 'New_York' + str(entry["Time"])
            )[0]


            # convert N Size string to an int
            num_voters = int(entry["N Size"].replace(",",""))
            # track sum of decided voders, use to calculate proper # of undecided
            num_decided_voters = 0

            for choice in choices:
                vote_percent = entry[choice]
                num_votes = int(vote_percent*num_voters)
                choice = Choice.objects.get_or_create(
                    question = question,
                    choice_text = choice
                )[0]
                choice.votes = num_votes
                choice.save()
                num_decided_voters += num_votes

            # calculate number of undecided voters and add to database
            choice = Choice.objects.get_or_create(
                question = question,
                choice_text = "Undecided"
            )[0]
            choice.votes = num_voters - num_decided_voters
            choice.save()

def parse_pollster_data(url):
    """ Extracts data from input pollster url to populate Question/Choice models
        in database. Should return the cursor for the next url."""

    # read data from input url
    response = read_url_data(url)
    data = json.loads(response.read())

    poll_entries = data["items"]

    next_cursor = data["next_cursor"]

    # for every poll entry, process data
    for poll_entry in poll_entries:

        # extract questions
        poll_questions = poll_entry["poll_questions"]

        # poll's slug
        poll_slug = poll_entry["slug"]


        # for each question, save the question and results
        for question_info in poll_questions:
            # question = Question.objects.get_or_create(
            question = Question.objects.get_or_create(
                question_text = question_info["text"],
                pub_date = parse_for_datetime(
                    question_info["question"]["created_at"]),
                slug = "{}: {}".format(
                    poll_slug,question_info["question"]["slug"]),
            )[0]

            poll_result = question_info["sample_subpopulations"][0]

            num_voters = poll_result["observations"]
            choices_list = poll_result["responses"]

            for choice_dict in choices_list:
                choice = Choice.objects.get_or_create(
                    question = question,
                    choice_text = choice_dict["text"],
                )[0]
                num_votes = int(choice_dict["value"]/100.0*num_voters)
                choice.votes = num_votes
                choice.save()
    return next_cursor


if __name__ == '__main__':

    rel_url = "parse_files/sample_text.json"
    abs_url = os.path.abspath(rel_url)
    url_local = "file://" + abs_url

    response = read_url_data(url_local)
    states_dict = parse_for_states(response)
    expected_states_dict = {"1":"California", "2":"California",
        "3":"New York", "4":"New York", "5":"Pennsylvania"}
    print(states_dict)
    print(states_dict == expected_states_dict)
