import unittest

from datasource import *

class TestDatasource(unittest.TestCase):

    def setUp(self):
        self.ds = DataSource("diiannic", "corn972corn")

    def test_valid_state_and_year(self):
        state = "Ohio"
        year = 2017
        self.assertTrue(self.ds.getNumberOfPeopleSurveyedByStateAndYear(state, year) > 1000)

    def test_invalid_state(self):
        state = "not state"
        self.assertRaises(AttributeError, self.ds.getNumberOfPeopleSurveyedByStateAndYear(state, 2018))

    def test_invalid_year(self):
        year = 1589
        self.assertFalse(self.ds.getNumberOfPeopleSurveyedByStateAndYear("Ohio", year) > 1000)

    def test_negative_year(self):
        year = -1
        self.assertFalse(self.ds.getNumberOfPeopleSurveyedByStateAndYear("Ohio", year) > 1000)

    def test_invalid_state_and_year(self):
        year = 1589
        state = "nope"
        self.assertRaises(AttributeError, self.ds.getNumberOfPeopleSurveyedByStateAndYear(state, year))


if __name__ == "__main__":
    unittest.main()
