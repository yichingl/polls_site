import unittest
from additional_test_files.parse_str import read_url_data

class ParseStrTestCase(unittest.TestCase):
    def setUp(self):
        self.text = read_url_data()

    def tearDown(self):
        pass;

    def test_contents_read_correctly(self):
        expected_text_excerpt = "[ { "
        read_text_excerpt = self.text.replace("\r\n", "")[0:len(expected_text_excerpt)]
        self.assertEqual(expected_text_excerpt, read_text_excerpt)

if __name__ == '__main__':
    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ParseStrTestCase)
