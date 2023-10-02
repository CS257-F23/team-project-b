import unittest
from Data import *
from ProductionCode.watch import *
import subprocess


class testFunctions(unittest.TestCase):
    
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

# First try at test (Most Likely will DELETE)
    '''def test_get_data_from_year(self): 
        """Test to make sure that the case details of all cases from the specified year are displayed"""
        output = CancerDataset.get_data_from_year(2002)
        self.assertEqual(output.get_year, 2002,
                         "Failed to display the corresponding data for specified year")'''

    def test_get_data_from_year(self):
        """ Tests the get_data_from_year function with a VALID year. Input: 2002 Expected output: all the cases corresponding to the year 2002"""
        data_file = CancerDataset("Data/dummy_file.csv")
        example_year = 2002
        output_from_tested_function = data_file.get_data_from_year(example_year)
        for cases in range(len(output_from_tested_function)):
            self.assertEqual(int(cases.get_year), 2002,
                             "Failed to display the corresponding data for specified year")
           
    def test_get_data_from_year_INVALID(self):
        """ Tests the get_data_from_year function with an INVALID year. Input: 3030 Expected output: [] (an empty list)"""
        data_file = CancerDataset("Data/dummy_file.csv")
        example_year = 3030
        output_from_get_data_from_year = data_file.get_data_from_year(example_year)
        self.assertEqual(output_from_get_data_from_year, [])
       

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
    
    def test_main_year(self):
        """Test for main() working for valid command line arguments for the year 2007. Due to the expected result's ENORMOUS size, only the last returned element is used to compare."""
        CLI_command_as_list = ['python3', 'ProductionCode/watch.py', "--year", "2007"]
        expected_result = 'State: Wyoming; Year: 2007; Leading Site: Urinary Bladder invasive and in situ; Sex: Male; Count: 103'
        failed_test_message = 'Failed to get data for the year 2007'
        def enter_CLI_command_return_code():
            return subprocess.Popen(CLI_command_as_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf8')
        def run_CLI_command_return_result():
            code = enter_CLI_command_return_code()
            output, err = code.communicate()
            code.terminate()
            return output.strip()[-103:-2]
        def execute_test():
            self.assertEqual(run_CLI_command_return_result(), expected_result, failed_test_message)
        execute_test()
    
    def test_main_site(self):
        """Test for main() working for valid command line arguments for the site 'Liver' (single quotes included). Due to the expected result's ENORMOUS size, only the last returned element is used to compare."""
        CLI_command_as_list = ['python3', 'ProductionCode/watch.py', "--site", "Liver"] # python3 ProductionCode/watch.py --site Liver
        expected_result = 'State: Wyoming; Year: 2020; Leading Site: Liver; Sex: Male; Count: 29'
        failed_test_message = "Failed to get data for the site 'Liver'."
        def enter_CLI_command_return_code():
            return subprocess.Popen(CLI_command_as_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf8')
        def run_CLI_command_return_result():
            code = enter_CLI_command_return_code()
            output, err = code.communicate()
            code.terminate()
            return output.strip()[-71:-2]
        def execute_test():
            self.assertEqual(run_CLI_command_return_result(), expected_result, failed_test_message)
        execute_test()
    
    

if __name__ == '__main__':
    unittest.main()
