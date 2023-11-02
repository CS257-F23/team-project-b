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
        result_from_function_being_tested = test.get_data_from_year(year_tested)
        expected_output = ('Wyoming', 2003, 'Ovary', 'Female', 38)
        error_message = "Failed to display the corresponding data for the specified year"
        self.assertIn(expected_output, result_from_function_being_tested, error_message)
    
    def test_get_data_from_year_INVALID(self):
        """Tests the get_data_from_year function with an INVALUD year. Input: 3030 Expected output: [] (an empty list)"""
        year_tested = 3030
        result_from_function_being_tested = test.get_data_from_year(year_tested)
        expected_output = []
        error_message = "Failed to display the corresponding data for the specified year"
        self.assertEqual(expected_output, result_from_function_being_tested, error_message)

    def test_get_total_for_year(self):
        """Tests the get_total_for_year function with a VALID year. Input: 2003 Expected output: 1277776"""
        year_tested = 2003
        result_from_function_being_tested = test.get_total_for_year(year_tested)
        expected_output = 1277776
        error_message = "Failed to display the corresponding data for the specified year"
        self.assertEqual(expected_output, result_from_function_being_tested, error_message)
    
    def test_get_total_for_year_edge_valid(self):
        """Tests the get_total_for_year function with a VALID edge case year. Input: 2000 Expected output: 1227167"""
        year_tested = 2000
        result_from_function_being_tested = test.get_total_for_year(year_tested)
        expected_output = 1227167
        error_message = "Failed to display the corresponding data for the specified year"
        self.assertEqual(expected_output, result_from_function_being_tested, error_message)

    def test_get_total_for_year_edge_invalid(self):
        """Tests the get_total_for_year function with an INVALID edge case year. Input: 2222 Expected output: None"""
        year_tested = 2222
        result_from_function_being_tested = test.get_total_for_year(year_tested)
        expected_output = None
        error_message = "Failed to display the corresponding data for the specified year"
        self.assertEqual(expected_output, result_from_function_being_tested, error_message)

class testGetSiteData(unittest.TestCase):
    setUp()
    def test_get_data_by_site(self):
        """Tests the get_data_by_site function with a VALID cancer site. Input: 'Myeloma' Expected output: List of cases which includes the expected_output variable"""
        site_tested = "Myeloma"
        result_from_function_being_tested = test.get_data_by_site(site_tested)
        expected_output = ('Wyoming', 2004, 'Myeloma', 'Male', 19)
        error_message = "Failed to display the corresponding data for specified site"
        self.assertIn(expected_output, result_from_function_being_tested, error_message)

    def test_get_data_by_site_INVALID(self):
        """Tests the get_data_by_site function with a INVALID cancer site. Input: 'Toe' Expected output: [] (an empty list)"""
        site_tested = "Toe"
        result_from_function_being_tested = test.get_data_by_site(site_tested)
        expected_output = []
        error_message = "Failed to display the corresponding data for specified site"
        self.assertEqual(expected_output, result_from_function_being_tested, error_message)
    
    def test_get_total_for_site(self):
        """Tests the get_total_for_site function with a VALID site. Input: 'Myeloma' Expected output: 469174"""
        site_tested = "Myeloma"
        result_from_function_being_tested = test.get_total_for_site(site_tested)
        expected_output = 469174
        error_message = "Failed to display the corresponding data for specified site"
        self.assertEqual(expected_output, result_from_function_being_tested, error_message)
   
    def test_get_total_for_site_edge_valid(self):
        """Tests the get_total_for_site function with a VALID edge case site. Input: 'Urinary Bladder, invasive and in situ' Expected output: 1473004"""
        site_tested = "Urinary Bladder invasive and in situ"
        result_from_function_being_tested = test.get_total_for_site(site_tested)
        expected_output = 1473004
        error_message = "Failed to display the corresponding data for specified site"
        self.assertEqual(expected_output, result_from_function_being_tested, error_message)

    def test_get_total_for_year_edge_invalid(self):
        """Tests the get_total_for_site function with an INVALID cancer site. Input: 'Body' Expected output: None"""
        site_tested = "Body"
        result_from_function_being_tested = test.get_total_for_site(site_tested)
        expected_output = None
        error_message = "Failed to display the corresponding data for specified site"
        self.assertEqual(expected_output, result_from_function_being_tested, error_message)

class testMixedCount(unittest.TestCase):
    setUp()
    def test_get_total_for_year_and_site(self):
        """Tests the get_total_for_year_and_site function with a VALID year and VALID cancer site. Input: 2000 and 'Breast' Expected output: 200035"""
        year_tested = 2000
        site_tested = "Breast"
        result_from_function_being_tested = test.get_total_for_year_and_site(year_tested, site_tested)
        expected_output = 200035
        error_message = "Failed to display the corresponding data for specified year and specified site"
        self.assertEqual(expected_output, result_from_function_being_tested, error_message)
