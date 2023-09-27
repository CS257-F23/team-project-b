"""
Important links:
https://docs.python.org/3/library/csv.html
https://anyaevostinar.github.io/classes/257-f23/project-command-line
"""

import csv

#not in final spot
file = 'Data/dummy_file.csv'
with open(file, 'r') as f: #opens csv file and reads is as a file
    all_lines = f.readlines()
    titles = all_lines.pop(0)   #removes first row of csv ans stores it in the list titles


def string_to_list(string_with_commas):
        """turns a string into a convenient list, so it can be indexed"""
        return string_with_commas.split(",")

class CancerDataset:  
    def __init__(self, data_name):
        file = data_name
        list_of_cases = []
    
    def make_lines(self):
        """opens the data file, and reads through each line of the file, outputting each to a list"""
        with open(file, 'r') as f: #opens csv file and reads is as a file
            all_lines = f.readlines() 
            return all_lines   #removes first row of csv and returns it it in the list titles
        
    def fill_list_of_cases(self):
        """adds individual cases to the list"""
        raw_data = self.make_lines()
        for i in range(len(raw_data)):
            line_entry = string_to_list(raw_data[i])
            case_entry = Case(line_entry[2],line_entry[3],line_entry[5],line_entry[7],line_entry[9])
            self.list_of_cases 

    
    
        
    

    def get_data_from_year(year): pass

class Case:
    def __init__(self, state, year, leading_site, sex, count):
        self.state = state
        self.year = year
        self.leading_site = leading_site
        self.sex = sex
        self.count = count
    
    def case_details(self): pass

# example codes
#case_example = Case("us", 2002, "mouth", "male", 2003)
#CancerDataset.dataset[1] = CancerDataset(case_example)




def main(): pass

