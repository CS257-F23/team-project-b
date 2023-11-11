import unittest
from app import *


class LoadData(unittest.TestCase):
    def setUp(self):
        load_data()
        self.app = app.test_client()

    """Helper function to reduce duplicated code. It runs the route provided and return the data of the resultant webpage."""

    def get_route_data(self, route):
        response = self.app.get(route, follow_redirects=True)
        return response.data


load_data()


class TestHomePage(LoadData):
    def test_home_page_route(self):
        """Test that the home page appears as expected and has the correct content."""
        url = '/'
        expected_portion = b"Welcome to our group's data analysis website"
        failure_response = "Failed to fetch the home page correctly."
        self.assertIn(expected_portion, self.get_route_data(
            url), failure_response)

    def test_home_page_route_edge_fail(self):
        """Test that the error page appears as expected when entering an unavailable URL and has the correct content."""
        url = '/nope'
        expected_portion = b"by mistake"
        failure_response = "Failed to fetch the error page correctly."
        self.assertIn(expected_portion, self.get_route_data(
            url), failure_response)


class TestYearDisplayPage(LoadData):
    def test_get_year_data_route(self):
        """Test that the year subset display page appears as expected in the normal case and has the correct content."""
        url = '/year/2007/'
        expected_portion = b"2007"
        failure_response = "Failed to fetch data for the year 2007 correctly."
        self.assertIn(expected_portion, self.get_route_data(
            url), failure_response)

    def test_get_year_data_route_edge_start(self):
        """Test that the year subset display page appears as expected in a working edge case at the starting end of the possible input and has the correct content."""
        url = '/year/2000/'
        expected_portion = b"2000"
        failure_response = "Failed to fetch data for the edge case year 2000 correctly."
        self.assertIn(expected_portion, self.get_route_data(
            url), self.get_route_data(url))

    def test_get_year_data_route_edge_end(self):
        """Test that the year subset display page appears as expected in a working edge case at the closing end of the possible input and has the correct content."""
        url = '/year/2020/'
        expected_portion = b"2020"
        failure_response = "Failed to fetch data for the edge case year 2021 correctly."
        self.assertIn(expected_portion, self.get_route_data(
            url), failure_response)

    def test_get_year_data_route_edge_fail(self):
        """Test that the error page appears as expected when entering an unavailable year URL and has the correct content."""
        url = '/year/1248/'
        expected_portion = b"The year that you have entered is invalid."
        failure_response = "The year that you have entered is invalid."
        self.assertIn(expected_portion, self.get_route_data(
            url), failure_response)


class TestSiteDisplayPage(LoadData):
    load_data()

    def test_get_site_data_route(self):
        """Test that the site subset display page appears as expected in the normal case and has the correct content."""
        url = '/site/Liver/'
        expected_portion = b"Liver"
        failure_response = "Failed to fetch data for the leading site 'Liver' correctly."
        self.assertIn(expected_portion, self.get_route_data(
            url), failure_response)

    def test_get_site_data_route_edge_start(self):
        """Test that the site subset display page appears as expected in a working edge case at the starting end of the possible input and has the correct content."""
        url = '/site/Brain and Other Nervous System/'
        expected_portion = b"Brain"
        failure_response = "Failed to fetch data for the edge case leading site 'Brain and Other Nervous System' correctly."
        self.assertIn(expected_portion, self.get_route_data(
            url), failure_response)

    def test_get_site_data_route_edge_end(self):
        """Test that the site subset display page appears as expected in a working edge case at the closing end of the possible input and has the correct content."""
        url = '/site/Urinary Bladder invasive and in situ/'
        expected_portion = b"Bladder"
        failure_response = "Failed to fetch data for the edge case leading site 'Urinary Bladder invasive and in situ' correctly."
        self.assertIn(expected_portion, self.get_route_data(
            url), failure_response)

    def test_get_site_data_route_edge_fail(self):
        """Test that the error page appears as expected when entering an unavailable site URL and has the correct content."""
        url = '/site/corpse/'
        expected_portion = b"here by mistake"
        failure_response = "Failed to fetch the error page correctly."
        self.assertIn(expected_portion, self.get_route_data(
            url), failure_response)


class TestAboutUsPage(LoadData):
    def test_about_us(self):
        """Tests that the about us page appears as expected and has the correct content."""
        url = '/about'
        expected_portion = b"This is our Cancer Incidences dataset navigation software"
        failure_response = "Failed to fetch the about us page correctly"
        self.assertIn(expected_portion, self.get_route_data(
            url), failure_response)


class TestContactUsPage(LoadData):
    def test_contact_us(self):
        """Tests that the contact us page appears as expected and has the correct content"""
        url = '/contact'
        expected_portion = b"Role: Fullstack developer"
        failure_response = "Failed to fetch the contact us page correctly"
        self.assertIn(expected_portion, self.get_route_data(
            url), failure_response)


class TestSimpleSearch(LoadData):
    def test_display_number_of_matches_with_form_data(self):
        """Test to make sure the simpsearch function renders the correct page through the form"""
        form_data = {'state': 'California',
                     'year': '2003', 'site': 'Liver', 'sex': 'Male'}
        response = self.app.post('/simpsearch', data=form_data)
        failure_response = "Failed to render the correct display page for the number of matches in simple search"
        self.assertEqual(response.status_code, 200, failure_response)

    def test_display_number_of_matches_with_nav_bar(self):
        """Test to make sure the simpsearch function renders the correct page through the nav bar"""
        response = self.app.get('/simpsearch')
        failure_response = "Failed to render the correct display page for the number of matches in simple search"
        self.assertEqual(response.status_code, 200, failure_response)


class TestStateInfo(LoadData):
    def test_state_info_display(self):
        """Test to make sure the state info page renders correctly through the form"""
        test_state = "Texas"
        response = self.app.post(
            '/stateinfo', data={'state_for_info_page': test_state})
        failure_response = "Failed to render the correct display page for the state chosen in the form"
        self.assertEqual(response.status_code, 200, failure_response)


class TestArgsHelperFunction(LoadData):
    def test_get_args_from_form_post(self):
        """Test to make sure the helper function works with POST"""
        response = self.app.post('/simpsearch',
                                 data={'state': 'california', 'year': '2003'})
        failure_response = "Failed to render correct page from POST"
        self.assertEqual(response.status_code, 200, failure_response)

    def test_get_args_from_form_normal_usage(self):
        """directly tests if requesting args (using get_args_from_form) returns expected list under normal conditions
        referenced: https://flask.palletsprojects.com/en/3.0.x/reqcontext/"""
        with app.test_request_context('/simpsearch', query_string={'state': 'Minnesota', 'site': 'Liver'}):
            args = get_args_from_form(['state', 'site'])
            failure_response = "Failed to retrieve args with function"
        self.assertEqual(args, ['Minnesota', 'Liver'], failure_response)

    def test_get_args_from_form_edge(self):
        """directly tests if requesting args (using get_args_from_form) returns expected list with no requests"""
        with app.test_request_context('/simpsearch', query_string={'state': 'Minnesota', 'site': 'Liver'}):
            args = get_args_from_form([])
            failure_response = "Failed to retrieve args with function"
        self.assertEqual(args, [], failure_response)

    def test_get_args_from_form_get(self):
        """Test to make sure the helper function works with GET"""
        response = self.app.get('/simpsearch')
        failure_response = "Failed to render correct page from GET"
        self.assertEqual(response.status_code, 200, failure_response)


if __name__ == '__main__':
    unittest.main()
