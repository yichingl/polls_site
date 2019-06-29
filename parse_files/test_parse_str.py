
import unittest
import os
# from additional_test_files.parse_str import read_url_data
from parse_str import read_url_data, parse_for_states, parse_for_very_consv, parse_for_2, parse_for_pol_lean_groups


class ParseStrTestCase(unittest.TestCase):
    def setUp(self):

        # Online data
        url_online = 'https://bbotllc.github.io/candidate-interviews/political_leanings.json'
        self.online_text = read_url_data(url_online).read().replace("\r","").replace("\n","")

        # Local data
        rel_url = "parse_files/sample_text.json"
        abs_url = os.path.abspath(rel_url)
        url_local = "file://" + abs_url

        # Pollster data
        url_pollster = "https://elections.huffingtonpost.com/pollster/api/v2/polls?cursor=16337&sort=created_at"
        self.pollster_text = read_url_data(url_pollster).read().replace("\r","").replace("\n","")

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
        expected_text_excerpt = '{"count":28464,'
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

    def test_parse_for_given_groups(self):
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



if __name__ == '__main__':
    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ParseStrTestCase)
