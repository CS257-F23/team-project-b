import unittest
from Data import *
from ProductionCode.watch import *


class testFunctions(unittest.TestCase):
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
        data_file = CancerDataset("dummy_file.csv")
        output = data_file.convert_dataset_into_titles_and_list_of_cases()
        self.assertEqual(output, expected_list,
                         "Failed fetching the expected list and convert it to a list of CSV strings.")

    def test_string_to_list_real_output(self):
        """Tests to make sure that the string to list function works in a real use case"""
        example = ",Alabama,1,2000,2000,Breast,26000,Female,F,2964\n"
        output = CancerDataset.split_data_string_to_list(example)
        self.assertEqual(output, ["", "Alabama", "1", "2000", "2000", "Breast",
                         "26000", "Female", "F", "2964"], "Failed to split a CSV line correctly.")

    def test_string_to_list_no_input(self):
        """Tests to make sure that the string to list function works in an edge case of no input"""
        example = ""
        output = CancerDataset.split_data_string_to_list(example)
        self.assertEqual(
            output, [], "Failed to return empty list for no input.")

    def create_text_file_for_test(self):
        file_name = "text_file.txt"
        file = open(file_name, "x")
        file.write("line 1")
        file.write("line 2")
        file.write("line 3")
        file.close()
        return file_name

    def test_file_reading(self):
        # opens csv file and reads is as a file
        with open(testFunctions.create_text_file_for_test(), 'r') as f:
            all_lines = f.readlines()
        expected_result = ["line 1\n",
                           "line 2\n",
                           "line 3\n",
                           ]
        self.assertEqual(all_lines, expected_result,
                         "Failed to correctly retrieve text file content.")

    def test_get_data_from_year(self):
        """Test to make sure that the case details of all cases from the specified year are displayed"""
        output = CancerDataset.get_data_from_year(2002)
        self.assertEqual(output.get_year, 2002,
                         "Failed to display the corresponding data for specified year")

    def test_get_data_by_site(self):
        "Test to make sure that the case details of all cases from the specified leading site are displayed"
        example_site = 'mouth'
        output = CancerDataset.get_data_by_site(example_site)
        self.assertEqual(output.get_leading_site, example_site,
                         "Failed to display the corresponding data for specified leading site")


if __name__ == '__main__':
    unittest.main()
