from urllib2 import urlopen




def read_url_data():
    """ Reads data at given url and returns a string containing contents. """

    url = 'https://bbotllc.github.io/candidate-interviews/political_leanings.json'
    try:
        response = urlopen(url)
        data_str = response.read()
    except urllib2.URLError as e:
        print(e.reason)
    except urllib2.HTTPError as e:
        print(e.code)
        print(e.read())

    return data_str


if __name__ == '__main__':
    data_str = read_url_data()
    print(data_str)
