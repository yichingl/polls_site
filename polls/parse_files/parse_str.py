import urllib2
import os
import re


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

    states_dict = {}

    regex_dict = {
    # "Geography": "(.+?)"
    # "Geography": "(?P<geography>.+?)"
        'geography': re.compile(r'"Geography": "(?P<geography>.+?)"')
    }

    line = response.readline()

    cnt = 1;
    while line:
        key, match = _parse_line(line, regex_dict)

        if match:
            states_dict[str(cnt)] = match.group('geography')
            cnt+=1;

        # increment
        line = response.readline()

    return states_dict



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
