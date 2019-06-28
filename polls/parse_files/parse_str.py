import urllib2
import os
import re

def get_json_parse(group, key_name):
    """ Given a key and group name, returns a json format regex string. """

    return '"{}": (?P<{}>.+?),'.format(group, key_name)

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

def _parse_line(line, regex_dict):
    """Matches regex dict keys with line contents, and returns key, match. """

    for key, regex_obj in regex_dict.items():
        match = regex_obj.search(line)
        if match:
            return key, match
    return None, None

def parse_for_states(response):
    """ Parses given response object and returns a dict containing
        entry# and state as key-value pairs. """

    group = "Geography"
    key_name = "key1"

    states_dict = {}
    group_key_dict = {"key1":group}

    regex_dict = {
        key_name: re.compile(r"{}".format(get_json_parse(group, key_name)))
    }

    line = response.readline()

    cnt = 1;
    while line:
        group, match = _parse_line(line, regex_dict)

        if match:
            states_dict[str(cnt)] = {group_key_dict[group]:match.group(group)}
            cnt+=1;

        # increment
        line = response.readline()

    return states_dict

def parse_for_very_consv(response):
    """ Parses given response object and returns a dict containing
        entry# and state as key-value pairs. """

    group = "Very conservative"
    key_name = "key1"

    consv_dict = {}
    group_key_dict = {"key1":group}

    regex_dict = {
        key_name: re.compile(r"{}".format(get_json_parse(group, key_name)))
    }

    line = response.readline()

    cnt = 1;
    while line:
        group, match = _parse_line(line, regex_dict)

        if match:
            consv_dict[str(cnt)] = {group_key_dict[group]:match.group(group)}
            cnt+=1;

        # increment
        line = response.readline()

    return consv_dict

def parse_for_2(response):
    """ Parses given response object and returns a dict containing
        entry# and state,consv as key-value pairs. """

    group1 = "Very conservative"
    key_name1 = "key1"

    group2 = "Geography"
    key_name2 = "key2"

    out_dict = {}
    group_key_dict = {key_name1:group1, key_name2:group2}

    regex_dict = {
        key_name1: re.compile(r"{}".format(get_json_parse(group1, key_name1))),
        key_name2: re.compile(r"{}".format(get_json_parse(group2, key_name2))),
    }

    line = response.readline()

    cnt = 1;
    while line:
        group, match = _parse_line(line, regex_dict)

        if match:

            # case for state match, which is first
            if group == key_name2: # geography
                out_dict[str(cnt)] = {group_key_dict[group]:match.group(group)}
            elif group == key_name1: # very conservative
                out_dict[str(cnt)][group_key_dict[group]] = match.group(group)
                # every entry has a "geography" and "very conservative" value
                # after both have been processed, increment entry count
                cnt += 1;

        # increment
        line = response.readline()

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
