"""
A collection of tests for the watch.py program. To run, navigate to /team-project-b/ and send 'python3 -m unittest discover Tests/' """
import unittest
from Data import *
from ProductionCode.watch import *
import subprocess


class testBasicFunctions(unittest.TestCase):
    def test_get_details(self):
        """Test to make sure that the get_details() method properly format the Case data."""
        test_state = "Alabama"
        test_year = "2000"
        test_site = "Breast"
        test_sex = "Female"
        test_count = "2964"
        test_case = Case(test_state, test_year, test_site, test_sex, test_count)
        expected_output = f"State: {test_state}; Year: {test_year}; Leading Site: {test_site}; Sex: {test_sex}; Count: {test_count}"
        self.assertEqual(test_case.get_details(), expected_output, "Failed formatting get_details().")
    
    def test_make_lines(self):
        """Test to make sure that data can be fetched from .csv file and converted to list of CSV strings"""
        expected_list = ("Notes,States,States Code,Year,Year Code,Leading Cancer Sites,Leading Cancer Sites Code,Sex,Sex Code,Count\n",
                         [",Alabama,1,2000,2000,Breast,26000,Female,F,2964\n",
                          ",Alabama,1,2003,2003,Myeloma,34000,Female,F,119\n",
                          ",Alaska,2,2006,2006,Lung and Bronchus,22030,Female,F,152\n",
                          ",Alaska,2,2011,2011,Melanoma of the Skin,25010,Male,M,40\n",
                          ",Alaska,2,2017,2017,Oral Cavity and Pharynx,20010-20100,Female,F,27\n",
                          ",Kansas,20,2009,2009,Thyroid,32010,Female,F,320\n",
                          ',New Mexico,35,2015,2015,"Urinary Bladder, invasive and in situ",29010,Female,F,95\n',
                          ',New Mexico,35,2016,2016,Oral Cavity and Pharynx,20010-20100,Male,M,170\n',
                          ',New York,36,2002,2002,Stomach,21020,Male,M,1088'
                          ]
                         )
        data_file = CancerDataset("Data/dummy_file.csv")
        output = data_file.convert_dataset_into_titles_and_list_of_cases()
        self.assertEqual(output, expected_list,
                         "Failed fetching the expected list and convert it to a list of CSV strings.")

class testStringToList(unittest.TestCase):
    def test_string_to_list_real_output(self):
        """Tests to make sure that the string to list function works in a real use case"""
        example = ",Alabama,1,2000,2000,Breast,26000,Female,F,2964\n"
        output = split_data_string_to_list(example)
        self.assertEqual(output, ["", "Alabama", "1", "2000", "2000", "Breast",
                         "26000", "Female", "F", "2964"], "Failed to split a CSV line correctly.")

    def test_string_to_list_no_input(self):
        """Tests to make sure that the string to list function works in an edge case of no input"""
        example = ""
        output = split_data_string_to_list(example)
        self.assertEqual(output, [""], "Failed to return empty list for no input.")

class testGetYearData(unittest.TestCase):
    def test_get_data_from_year(self):
        """ Tests the get_data_from_year function with a VALID year. Input: 2002 Expected output: all the cases corresponding to the year 2002"""
        data_file = CancerDataset("Data/dummy_file.csv")
        example_year = 2002
        output_from_tested_function = data_file.get_data_from_year(example_year)
        expected_output = ['State: New York; Year: 2002; Leading Site: Stomach; Sex: Male; Count: 1088']
        self.assertEqual(expected_output, output_from_tested_function, "Failed to display the corresponding data for specified year")
        # for cases in range(len(output_from_tested_function)):
        #     self.assertEqual(int(cases.get_year()), 2002,
        #                      "Failed to display the corresponding data for specified year")
           
    def test_get_data_from_year_INVALID(self):
        """ Tests the get_data_from_year function with an INVALID year. Input: 3030 Expected output: [] (an empty list)"""
        data_file = CancerDataset("Data/dummy_file.csv")
        example_year = 3030
        output_from_get_data_from_year = data_file.get_data_from_year(example_year)
        self.assertEqual(output_from_get_data_from_year, [])
       
class testGetSiteData(unittest.TestCase):
    def test_get_data_by_site(self):
        """ Tests the get_data_by_site function with a VALID cancer site. Input: mouth Expected output: all the cases where the leading cancer site is mouth """
        data_file = CancerDataset("Data/dummy_file.csv")
        example_site = 'mouth'
        output_from_tested_function = data_file.get_data_by_site(example_site)
        for cases in range(len(output_from_tested_function)):
            self.assertEqual(cases.get_leading_site, example_site,
                             "Failed to display the corresponding data for specified leading site")
           
    def test_get_data_by_site_INVALID(self):
        """ Tests the get_data_by_site function with a INVALID cancer site. Input: toe Expected output: [] (an empty list)"""
        data_file = CancerDataset("Data/dummy_file.csv")
        example_site = 'toe'
        output_from_get_data_by_site = data_file.get_data_by_site(example_site)
        self.assertEqual(output_from_get_data_by_site, [])

class testCounts(unittest.TestCase):
    def test_get_total_for_year_and_site(self):
        data_file = CancerDataset("Data/clean_incidence.csv")
        test_site = "Liver"
        test_year = 2000
        expected_result = 11780
        output_from_get_total_for_year_and_site = data_file.get_total_for_year_and_site(test_year, test_site)
        self.assertEqual(output_from_get_total_for_year_and_site, expected_result)

class TestCaseClass(unittest.TestCase):
    global dummy_case
    dummy_case = Case("Minnesota","2000","Liver","Female","2")
    
    def test_get_details(self): 
        self.assertEqual(dummy_case.get_details(), "State: Minnesota; Year: 2000; Leading Site: Liver; Sex: Female; Count: 2", "Failed to get details of a Case.")
    
    def test_get_state(self): 
        self.assertEqual(dummy_case.get_state(), "Minnesota", "Failed to get the state of a Case.")
    
    def test_get_year(self): 
        self.assertEqual(dummy_case.get_year(), "2000", "Failed to get the year of a Case.")
    
    def test_get_leading_site(self): 
        self.assertEqual(dummy_case.get_leading_site(), "Liver", "Failed to get the leading site of a Case.")
    
    def test_get_sex(self): 
        self.assertEqual(dummy_case.get_sex(), "Female", "Failed to get the sex of a Case victim.")
    
    def test_get_count(self): 
        self.assertEqual(dummy_case.get_count(), "2", "Failed to get the cou of a Case victim.")
    
    def test_verify_match_user_input_and_normal_input(self):
        """simple test to make sure that the verify match user input works given the and parameter"""
        function_output = dummy_case.verify_match_user_input("and",["Minnesota","2000","Liver"])
        desired_output = {'result': True, 'matched': ["Minnesota","2000","Liver"]}
        self.assertEqual(function_output,desired_output)

    def test_verify_match_user_input_and_none_matching(self):
        """simple test to make sure that the verify match user input works given the and parameter"""
        function_output = dummy_case.verify_match_user_input("and",["The U.s.","2222","Whole Body"])
        desired_output = {'result': False, 'matched': []}
        self.assertEqual(function_output,desired_output)


class testGreatFilter(unittest.TestCase):
    """Includes tests related to the great filter functionality"""
    global dataset
    dataset = CancerDataset("Data/clean_incidence.csv")
    
    def run_URL_and_assert_total_count(self, combination_method, target_datas, expected_count):
        """Helper function to the various tests for the Great Filter. Accept the supposed user inputs and assertEqual() the resultant total count as they are highly unprobable to repeat with 2 different input."""
        function_output = dataset.get_total_and_details(combination_method, target_datas)
        self.assertEqual(function_output['total count'], expected_count)

    def test_get_total_and_details_normal_value_and(self):
        combination_method = "and"
        target_datas = ["Alabama","Male","Liver","2000"]
        expected_count = 122
        self.run_URL_and_assert_total_count(combination_method, target_datas, expected_count)
    
    def test_get_total_and_details_normal_value_or(self):
        """tests to see if the get total and details works with expected values using the 'or' combination"""
        combination_method = "or"
        target_datas = ["Alabama","Male","Liver","2000"]
        expected_count = 16248858
        self.run_URL_and_assert_total_count(combination_method, target_datas, expected_count)
    
    def test_get_total_and_details_normal_value_edge_one_input(self):
        """tests to see if the get total and details works with 1 expected value. Both /and/ and /or/ will retrun the same value"""
        combination_method = "or"
        target_datas = ["Alabama"]
        expected_count = 472138
        self.run_URL_and_assert_total_count(combination_method, target_datas, expected_count)
    
    def test_get_total_and_details_normal_value_edge_all_output(self):
        """tests to see if the get total and details works with input that return the whole dataset. Both /and/ and /or/ will retrun the same value as long as all possible input of any one field is used."""
        combination_method = "and"
        target_datas = ["Male","Female"]
        expected_count = 29913206
        self.run_URL_and_assert_total_count(combination_method, target_datas, expected_count)
    
    
    
    
    
    
    
    


class testMain(unittest.TestCase):
    def run_CLI_command_return_result(self, CLI_command_as_list):
        """Helper function to accept a list of string containing CLI inputs and return the expected result in the form of a string."""
        code = subprocess.Popen(CLI_command_as_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf8')
        output, err = code.communicate()
        code.terminate()
        return output.strip()
    
    def test_main_year(self):
        """Test for main() working for valid command line arguments for the year 2007. Due to the expected result's ENORMOUS size, only the last returned element is used to compare."""
        CLI_command_as_list = ['python3', 'ProductionCode/watch.py', "--year", "2007"]
        expected_result = 'State: Wyoming; Year: 2007; Leading Site: Urinary Bladder invasive and in situ; Sex: Male; Count: 103'
        failed_test_message = 'Failed to get data for the year 2007'
        self.assertIn(expected_result, self.run_CLI_command_return_result(CLI_command_as_list), failed_test_message)
    
    def test_main_year_edge(self):
        """Test for main() working for edge case command line arguments for an invalid year (3007)."""
        CLI_command_as_list = ['python3', 'ProductionCode/watch.py', "--year", "3007"]
        expected_result = ''
        failed_test_message = 'Failed to return empty string for --year edge case.'
        self.assertIn(expected_result, self.run_CLI_command_return_result(CLI_command_as_list), failed_test_message)
    
    def test_main_site(self):
        """Test for main() working for valid command line arguments for the site 'Liver' (single quotes included). Due to the expected result's ENORMOUS size, only the last returned element is used to compare."""
        CLI_command_as_list = ['python3', 'ProductionCode/watch.py', "--site", "Liver"] # python3 ProductionCode/watch.py --site Liver
        expected_result = 'State: Wyoming; Year: 2020; Leading Site: Liver; Sex: Male; Count: 29'
        failed_test_message = "Failed to get data for the site 'Liver'."
        self.assertIn(expected_result, self.run_CLI_command_return_result(CLI_command_as_list), failed_test_message)
    
    def test_main_site_edge(self):
        """Test for main() working for edge case command line arguments for an invalid site (Planet)."""
        CLI_command_as_list = ['python3', 'ProductionCode/watch.py', "--site", "Planet"]
        expected_result = ''
        failed_test_message = 'Failed to return empty string for --site edge case.'
        self.assertIn(expected_result, self.run_CLI_command_return_result(CLI_command_as_list), failed_test_message)
    
    

if __name__ == '__main__':
    unittest.main()