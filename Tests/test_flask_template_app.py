import unittest
from app import *

class LoadData(unittest.TestCase):
    def setUp(self):
        load_data()
    
    """Helper function to reduce duplicated code. It runs the route provided and return the data of the resultant webpage."""
    def get_route_data (self, route):
        self.app = app.test_client()
        response = self.app.get(route, follow_redirects=True)
        return response.data

load_data()

class TestHomePage(LoadData):
    def test_home_page_route(self):
        """Test that the home page appears as expected and has the correct content."""
        url = '/'
        expected_portion = b"For a more in-depth introduction"
        failure_response = "Failed to fetch the home page correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)
    
    def test_home_page_route_edge_fail(self):
        """Test that the error page appears as expected when entering an unavailable URL and has the correct content."""
        url = '/nope'
        expected_portion = b"by mistake"
        failure_response = "Failed to fetch the error page correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)
    
class TestYearDisplayPage(LoadData):
    def test_get_year_data_route(self):
        """Test that the year subset display page appears as expected in the normal case and has the correct content."""
        url = '/year/2007/'
        expected_portion = b"Year: 2007"
        failure_response = "Failed to fetch data for the year 2007 correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)
    
    def test_get_year_data_route_edge_start(self):
        """Test that the year subset display page appears as expected in a working edge case at the starting end of the possible input and has the correct content."""
        url = '/year/2000/'
        expected_portion = b"Year: 2000"
        failure_response = "Failed to fetch data for the edge case year 2000 correctly."
        self.assertIn(expected_portion, self.get_route_data(url), self.get_route_data(url))
    
    def test_get_year_data_route_edge_end(self):
        """Test that the year subset display page appears as expected in a working edge case at the closing end of the possible input and has the correct content."""
        url = '/year/2020/'
        expected_portion = b"Year: 2020"
        failure_response = "Failed to fetch data for the edge case year 2021 correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)
    
    def test_get_year_data_route_edge_fail(self):
        """Test that the error page appears as expected when entering an unavailable year URL and has the correct content."""
        url = '/year/1248/'
        expected_portion = b"The year that you have entered is invalid."
        failure_response = "The year that you have entered is invalid."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response) 

class TestSiteDisplayPage(LoadData):
    load_data()
    def test_get_site_data_route(self):
        """Test that the site subset display page appears as expected in the normal case and has the correct content."""
        url = '/site/Liver/'
        expected_portion = b"Below, you can see a portion of our dataset, filtered for those that match the leading site 'Liver':"
        failure_response = "Failed to fetch data for the leading site 'Liver' correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)
        
    def test_get_site_data_route_edge_start(self):
        """Test that the site subset display page appears as expected in a working edge case at the starting end of the possible input and has the correct content."""
        url = '/site/Brain and Other Nervous System/'
        expected_portion = b"Leading Site: Brain and Other Nervous System"
        failure_response = "Failed to fetch data for the edge case leading site 'Brain and Other Nervous System' correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)
    
    def test_get_site_data_route_edge_end(self):
        """Test that the site subset display page appears as expected in a working edge case at the closing end of the possible input and has the correct content."""
        url = '/site/Urinary Bladder invasive and in situ/'
        expected_portion = b"Leading Site: Urinary Bladder invasive and in situ"
        failure_response = "Failed to fetch data for the edge case leading site 'Urinary Bladder invasive and in situ' correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)        
    
    def test_get_site_data_route_edge_fail(self):
        """Test that the error page appears as expected when entering an unavailable site URL and has the correct content."""
        url = '/site/corpse/'
        expected_portion = b"here by mistake"
        failure_response = "Failed to fetch the error page correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)

class TestGreatFilterDisplayPage(LoadData):
    def test_get_data_route(self):
        """Test that the info display page appears as expected in the normal case and has the correct content."""
        url = '/and/Liver/'
        expected_portion = b"This is our information display page"
        failure_response = "Failed to fetch data for the leading site 'Liver' correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)
        
    def test_get_data_route_whitespaces(self):
        """Test that the info display page appears as expected in the normal case and has the correct content with extra whitespaces."""
        url = '/and/ Liver , Alabama/'
        expected_portion = b"This is our information display page"
        failure_response = "Failed to fetch data for the leading site 'Liver' correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)
        
    def test_get_data_route_edge_one(self):
        """Test that the info display page appears as expected in a working edge case at only 1 input."""
        url = '/or/Brain and Other Nervous System/'
        expected_portion = b"This is our information display page"
        failure_response = "Failed to fetch data for the edge case leading site 'Brain and Other Nervous System' correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)
    
    def test_get_data_route_edge_all(self):
        """Test that the site subset display page appears as expected in a working edge case at input that output all of the full dataset."""
        url = '/or/Male,Female/'
        expected_portion = b"This is our information display page"
        failure_response = "Failed to fetch data for the edge case leading site 'Urinary Bladder invasive and in situ' correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)        
    
    def test_get_data_route_edge_fail(self):
        """Test that the error page appears as expected when entering an unavailable site URL and has the correct content."""
        url = '/and/L1ver'
        expected_portion = b"by mistake"
        failure_response = "Failed to fetch the error page correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)
    
    def test_get_data_route_edge_nothing(self):
        """Test that the error page appears as expected when not entering anything after the combination method."""
        url = '/and/nothing'
        expected_portion = b"by mistake"
        failure_response = "Failed to fetch the error page correctly."
        self.assertIn(expected_portion, self.get_route_data(url), failure_response)
    
if __name__ == '__main__':
    unittest.main()
