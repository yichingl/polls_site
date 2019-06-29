import urllib2
import os
import re
import json


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

def parse_for_pollster_groups(response):
    """ Parses given response object and returns a dict containing
        entry# and group data as key-value pairs. """

    data = json.loads(response.read())

    out_dict = {}

    # parse poll data
    out_dict["cursor"] = data["cursor"]
    out_dict["next_cursor"] = data["next_cursor"]

    poll_entries = data["items"]

    qnum = 1;
    for poll_entry in poll_entries:


        # extract questions
        question_groups = poll_entry["poll_questions"]

        for question_info in question_groups:
            question_entry_dict = {}
            question_entry_dict["poll_question_text"] = question_info["text"]
            question_entry_dict["poll_responses"] = question_info["sample_subpopulations"]

            out_dict[qnum] = question_entry_dict
            qnum += 1
    return out_dict


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
