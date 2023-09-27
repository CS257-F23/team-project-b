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




class CancerDataset:  
    def __init__(self, data_name):
        file = data_name
        list_of_cases = []
        
        
    
    def create_entire_dataset():
        with open(file, 'r') as f: #opens csv file and reads is as a file
            all_lines = f.readlines() 
            titles = all_lines.pop(0)   #removes first row of csv ans stores it in the list titles
        entire_dataset = []
        pass
    

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

