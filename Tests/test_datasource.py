import unittest
from Data import *
from ProductionCode.datasource import DataSource

def setUp():
    global test
    test = DataSource()


class testGetYearData(unittest.TestCase):
    setUp()
    def test_get_data_from_year(self):
        """Tests the get_data_from_year function with a VALID year. Input: 2003 Expected output: List of cases which includes the expected_output variable"""
        year_tested = 2003
        test_result = test.get_data_from_year(year_tested)
        expected_output = ('Wyoming', 2003, 'Ovary', 'Female', 38)
        error_message = "Failed to display the corresponding data for the specified year"
        self.assertIn(expected_output, test_result, error_message)
    
    def test_get_data_from_year_INVALID(self):
        """Tests the get_data_from_year function with an INVALUD year. Input: 3030 Expected output: [] (an empty list)"""
        year_tested = 3030
        test_result = test.get_data_from_year(year_tested)
        expected_output = []
        error_message = "Failed to display the corresponding data for the specified year"
        self.assertEqual(expected_output, test_result, error_message)

    def test_get_total_for_year(self):
        """Tests the get_total_for_year function with a VALID year. Input: 2003 Expected output: 1277776"""
        year_tested = 2003
        test_result = test.get_total_for_year(year_tested)
        expected_output = 1277776
        error_message = "Failed to display the corresponding number of cases for the specified year"
        self.assertEqual(expected_output, test_result, error_message)
    
    def test_get_total_for_year_edge_valid(self):
        """Tests the get_total_for_year function with a VALID edge case year. Input: 2000 Expected output: 1227167"""
        year_tested = 2000
        test_result = test.get_total_for_year(year_tested)
        expected_output = 1227167
        error_message = "Failed to display the corresponding number of cases for the specified year"
        self.assertEqual(expected_output, test_result, error_message)

    def test_get_total_for_year_edge_invalid(self):
        """Tests the get_total_for_year function with an INVALID edge case year. Input: 2222 Expected output: None"""
        year_tested = 2222
        test_result = test.get_total_for_year(year_tested)
        expected_output = None
        error_message = "Failed to display the corresponding number of cases for the specified year"
        self.assertEqual(expected_output, test_result, error_message)

class testGetSiteData(unittest.TestCase):
    setUp()
    def test_get_data_by_site(self):
        """Tests the get_data_by_site function with a VALID cancer site. Input: 'Myeloma' Expected output: List of cases which includes the expected_output variable"""
        site_tested = "Myeloma"
        test_result = test.get_data_by_site(site_tested)
        expected_output = ('Wyoming', 2004, 'Myeloma', 'Male', 19)
        error_message = "Failed to display the corresponding data for specified site"
        self.assertIn(expected_output, test_result, error_message)

    def test_get_data_by_site_INVALID(self):
        """Tests the get_data_by_site function with a INVALID cancer site. Input: 'Toe' Expected output: [] (an empty list)"""
        site_tested = "Toe"
        test_result = test.get_data_by_site(site_tested)
        expected_output = []
        error_message = "Failed to display the corresponding data for specified site"
        self.assertEqual(expected_output, test_result, error_message)
    
    def test_get_total_for_site(self):
        """Tests the get_total_for_site function with a VALID site. Input: 'Myeloma' Expected output: 469174"""
        site_tested = "Myeloma"
        test_result = test.get_total_for_site(site_tested)
        expected_output = 469174
        error_message = "Failed to display the corresponding number of cases for specified site"
        self.assertEqual(expected_output, test_result, error_message)
   
    def test_get_total_for_site_edge_valid(self):
        """Tests the get_total_for_site function with a VALID edge case site. Input: 'Urinary Bladder invasive and in situ' Expected output: 1473004"""
        site_tested = "Urinary Bladder invasive and in situ"
        test_result = test.get_total_for_site(site_tested)
        expected_output = 1473004
        error_message = "Failed to display the corresponding number of cases for specified site"
        self.assertEqual(expected_output, test_result, error_message)

    def test_get_total_for_year_edge_invalid(self):
        """Tests the get_total_for_site function with an INVALID edge case cancer site. Input: 'Body' Expected output: None"""
        site_tested = "Body"
        test_result = test.get_total_for_site(site_tested)
        expected_output = None
        error_message = "Failed to display the corresponding number of cases for specified site"
        self.assertEqual(expected_output, test_result, error_message)

class testGetStateData(unittest.TestCase):
    setUp()
    def test_get_total_for_state(self):
        """Tests the get_total_for_state function with a VALID state. Input: 'Texas' Expected output: 1947730"""
        state_tested = "Texas"
        test_result = test.get_total_for_state(state_tested)
        expected_output = 1947730
        error_message = "Failed to display the corresponding number of cases for specified state"
        self.assertEqual(expected_output, test_result, error_message)

    def test_get_total_for_state_edge_valid(self):
        """Tests the get_total_for_state function with a VALID edge case state. Input: 'Alabama' Expected output: 472138"""
        state_tested = "Alabama"
        test_result = test.get_total_for_state(state_tested)
        expected_output = 472138
        error_message = "Failed to display the corresponding number of cases for specified state"
        self.assertEqual(expected_output, test_result, error_message)

    def test_get_total_for_state_edge_invalid(self):
        """Tests the get_total_for_state function with an INVALID edge case state. Input: 'Alibaba' Expected output: None"""
        state_tested = "Alibaba"
        test_result = test.get_total_for_state(state_tested)
        expected_output = None
        error_message = "Failed to display the corresponding number of cases for specified state"
        self.assertEqual(expected_output, test_result, error_message)

    def test_get_ranked_list_for_state(self):
        """Tests the get_ranked_list_for_state function with a VALID state. Input: 'Texas' Expected output: List of cases which includes the expected_output variable"""
        state_tested = "Texas"
        test_result = test.get_ranked_list_for_state(state_tested)
        expected_output = ('Breast', 315066)
        error_message = "Failed to display the corresponding top 10 list for the specified state"
        self.assertIn(expected_output, test_result, error_message)

class testSimpleSearchAndFeatures(unittest.TestCase):
    setUp()
    def test_get_simple_search_data(self):
        """Tests the get_simple_search_data function with a VALID state, year, and site. Input: '['Texas','2005','Liver','Male']' Expected Output: 1129"""
        input_targets_tested = ["Texas","2005","Liver","Male"]
        test_result = test.get_simple_search_data(input_targets_tested)
        expected_output = 1129
        error_message = "Failed to display the corresponding count for the simple search using the specified state, year, and site"
        self.assertEqual(expected_output, test_result, error_message)