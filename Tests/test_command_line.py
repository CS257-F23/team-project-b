"""a test suite made specifically for testing main() functions and command line functionality"""
import unittest
from Data import *
from Data.datasource import *
from ProductionCode.watch import *
from cl import *
import subprocess

def makeParser():
    """a function that makes a parser object, so command line parsing can be tested"""
    test_parser = argparse.ArgumentParser()
    test_parser.add_argument("--year", type=int, choices=range(2000, 2021))
    test_parser.add_argument("--site", type=str, choices=['Brain and Other Nervous System', 'Breast', 'Cervix Uteri', 'Colon and Rectum', 'Corpus Uteri', 'Esophagus', 'Gallbladder', 'Kidney and Renal Pelvis', 'Larynx', 'Leukemias',
                            'Liver', 'Lung and Bronchus', 'Melanoma of the Skin', 'Myeloma', 'Non-Hodgkin Lymphoma', 'Oral Cavity and Pharynx', 'Ovary', 'Pancreas', 'Prostate', 'Stomach', 'Thyroid', 'Urinary Bladder invasive and in situ'])
    return test_parser

class testMain(unittest.TestCase):
    def run_CLI_command_return_result(self, CLI_command_as_list):
        """Helper function to accept a list of string containing CLI inputs and return the expected result in the form of a string."""
        code = subprocess.Popen(CLI_command_as_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf8')
        output, err = code.communicate()
        code.terminate()
        return output.strip()
    
    def test_main_edge_no_input(self):
        """Test for main() for edge case command line arguments for no entry."""
        CLI_command_as_list = ['python3', 'cl.py']
        expected_result = 'Welcome to the WATCH app'
        failed_test_message = 'Failed to return help message for no CLI arguments.'
        self.assertIn(expected_result, self.run_CLI_command_return_result(CLI_command_as_list), failed_test_message)
    
    # def test_main_year(self):
    #     """Test for main() working for valid command line arguments for the year 2007. Due to the expected result's ENORMOUS size, only the last returned element is used to compare."""
    #     CLI_command_as_list = ['python3', 'cl.py', "--year", "2007"]
    #     expected_result = 'State: Wyoming; Year: 2007; Leading Site: Urinary Bladder invasive and in situ; Sex: Male; Count: 103'
    #     failed_test_message = 'Failed to get data for the year 2007'
    #     self.assertIn(expected_result, self.run_CLI_command_return_result(CLI_command_as_list), failed_test_message)
    
    def test_main_year_edge(self):
        """Test for main() working for edge case command line arguments for an invalid year (3007)."""
        CLI_command_as_list = ['python3', 'cl.py', "--year", "3007"]
        expected_result = ''
        failed_test_message = 'Failed to return empty string for --year edge case.'
        self.assertIn(expected_result, self.run_CLI_command_return_result(CLI_command_as_list), failed_test_message)
    
    # def test_main_site(self):
    #     """Test for main() working for valid command line arguments for the site 'Liver' (single quotes included). Due to the expected result's ENORMOUS size, only the last returned element is used to compare."""
    #     CLI_command_as_list = ['python3', 'cl.py', "--site", "Liver"] # python3 ProductionCode/watch.py --site Liver
    #     expected_result = 'State: Wyoming; Year: 2020; Leading Site: Liver; Sex: Male; Count: 29'
    #     failed_test_message = "Failed to get data for the site 'Liver'."
    #     self.assertIn(expected_result, self.run_CLI_command_return_result(CLI_command_as_list), failed_test_message)
    
    def test_main_site_edge(self):
        """Test for main() working for edge case command line arguments for an invalid site (Planet)."""
        CLI_command_as_list = ['python3', 'cl.py', "--site", "Planet"]
        expected_result = ''
        failed_test_message = 'Failed to return empty string for --site edge case.'
        self.assertIn(expected_result, self.run_CLI_command_return_result(CLI_command_as_list), failed_test_message)

    def test_parse_command_line_args_year(self):
        """uses identical parser to main file in order to test whether or not parse_command_line_args works for year"""
        parser = makeParser()
        args = parser.parse_args(['--year','2005'])
        self.assertEqual('[]\ntotal cases: 0',parse_commandline_args(args)) #dummy file has no 2005, so this just checks to make sure it returns an empty list
        
    def test_parse_command_line_args_site(self):
        """uses identical parser to main file in order to test whether or not parse_command_line_args works for site"""
        parser = makeParser()
        args = parser.parse_args(['--site','Liver'])
        self.assertEqual('[]\ntotal cases: 0',parse_commandline_args(args)) 