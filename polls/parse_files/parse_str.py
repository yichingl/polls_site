import urllib2
import os


def read_url_data(url):
    """ Reads data at given url and returns a string containing contents. """

    try:
        response = urllib2.urlopen(url)
        data_str = response.read().replace("\r","").replace("\n","")
        return data_str
    except urllib2.URLError as e:
        print(e.reason)
    except urllib2.HTTPError as e:
        print(e.code)
        print(e.read())



if __name__ == '__main__':

    rel_url = "parse_files/sample_text.json"
    abs_url = os.path.abspath(rel_url)
    url_local = "file://" + abs_url

    data_str = read_url_data(url_local)
    print(data_str)
