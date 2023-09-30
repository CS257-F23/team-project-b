import unittest
from Data import *
from ProductionCode.watch import *


class testFunctions(unittest.TestCase):
    def test_make_lines(self):
        """Test to make sure that data can be fetched from .csv file and converted to list of CSV strings"""
        expected_list = ['Notes,States,States Code,Year,Year Code,Leading Cancer Sites,Leading Cancer Sites Code,Sex,Sex Code,Count\n', 
                         ",Alabama,1,2000,2000,Breast,26000,Female,F,2964\n",
                         ",Alabama,1,2003,2003,Myeloma,34000,Female,F,119\n",
                         ",Alaska,2,2006,2006,Lung and Bronchus,22030,Female,F,152\n",
                         ",Alaska,2,2011,2011,Melanoma of the Skin,25010,Male,M,40\n",
                         ",Alaska,2,2017,2017,Oral Cavity and Pharynx,20010-20100,Female,F,27\n",
                         ",Kansas,20,2009,2009,Thyroid,32010,Female,F,320\n",
                         ',New Mexico,35,2015,2015,"Urinary Bladder, invasive and in situ",29010,Female,F,95\n',
                         ',New Mexico,35,2016,2016,Oral Cavity and Pharynx,20010-20100,Male,M,170\n',
                         ',New York,36,2002,2002,Stomach,21020,Male,M,1088'
                         ]
        data_file = CancerDataset("dummy_file.csv")
        output = data_file.convert_dataset_into_titles_and_list_of_cases()
        self.assertEqual(output,expected_list,"Failed fetching the expected list and convert it to a list of CSV strings.")

    def test_string_to_list_real_output(self):
        """Tests to make sure that the string to list function works in a real use case"""
        example = ",Alabama,1,2000,2000,Breast,26000,Female,F,2964\n"
        output = split_data_string_to_list(example)
        self.assertEqual(output,["","Alabama","1","2000","2000","Breast","26000","Female","F","2964"], "Failed to split a CSV line correctly.")
    
    def test_string_to_list_no_input(self):
        """Tests to make sure that the string to list function works in an edge case of no input"""
        example = ""
        output = split_data_string_to_list(example)
        self.assertEqual(output,[], "Failed to return empty list for no input.")


# test that pop works
# = [1,2,3]
#print (test.pop(0))

# test that .readlines() convert the whole .csv to lines
#with open(file, 'r') as f: #opens csv file and reads is as a file
    #all_lines = f.readlines() 

if __name__ == '__main__':
    unittest.main()