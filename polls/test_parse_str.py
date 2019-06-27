import unittest
import os
from additional_test_files.parse_str import read_url_data

class ParseStrTestCase(unittest.TestCase):
    def setUp(self):

        rel_url = "additional_test_files/sample_text.json"
        abs_url = os.path.abspath(rel_url)
        url_local = "file://" + abs_url

        url_online = 'https://bbotllc.github.io/candidate-interviews/political_leanings.json'

        self.local_text = read_url_data(url_local)
        self.online_text = read_url_data(url_online)

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

if __name__ == '__main__':
    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ParseStrTestCase)
