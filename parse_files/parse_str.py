import urllib2
import os
import re
import json
import datetime

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

def parse_for_ny_data(response):
    """ Parses given political_leanings response object and returns a
        dict containing entry# and question/answers data as key-value pairs. """

    data = json.loads(response.read())

    list_of_groups = ["Very conservative","Conservative, (or)",
        "Moderate","Liberal, (or)", "Very liberal", "NA", "N Size", "Time"]

    entries = []
    for entry in data:

        if entry["Geography"] == "New York":
            entry_dict = {}
            for group in list_of_groups:
                entry_dict[group] = entry[group]
            entries.append(entry_dict)

    return entries


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
