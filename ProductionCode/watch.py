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


def split_data_string_to_list(string_with_commas):
        """Split a string read from the .csv file into a convenient list, so it can be indexed. It also removes new line, if that's at the end of the last item"""
        split_entry = string_with_commas.split(",")
        #if split_entry[9][len(split_entry[9])-1] == "\n":
        split_entry[-1] = split_entry[-1].rstrip("\n")
        return split_entry

class Case:
    def __init__(self, state, year, leading_site, sex, count):
        self.state = state
        self.year = year
        self.leading_site = leading_site
        self.sex = sex
        self.count = count
    
    def case_details(self): pass

class CancerDataset:  
    def __init__(self, dataset_name):
        self.file = dataset_name # the .csv dataset file being accessed for the data
        self.list_of_cases = [] # list of cases, each of which is stored as a Case instance
    
    def convert_dataset_into_titles_and_list_of_cases(self):
        """opens the data file, and reads through each line of the file, outputting each to a list"""
        with open(self.file, 'r') as f: #opens csv file and reads is as a file
            all_lines = f.readlines() # get all the lines form the file
            return all_lines[0], all_lines[1:]   #removes first row of csv and returns it in the list titles
        
    def fill_list_of_cases(self):
        """adds individual Case instances to the list"""
        titles, raw_data = self.convert_dataset_into_titles_and_list_of_cases()
        for i in range(len(raw_data)):
            line_entry = split_data_string_to_list(raw_data[i])
            case_entry = Case(line_entry[2],line_entry[3],line_entry[5],line_entry[7],line_entry[9])
            self.list_of_cases.append(case_entry)

    def get_data_from_year(year): pass

# example codes
#case_example = Case("us", 2002, "mouth", "male", 2003)
#CancerDataset.dataset[1] = CancerDataset(case_example)




def main(): pass

