"""
Important links:
https://docs.python.org/3/library/csv.html
https://anyaevostinar.github.io/classes/257-f23/project-command-line
"""

import csv
import argparse

parser = argparse.ArgumentParser()
#referenced realPython tutorial for CLI implementation.
parser.add_argument("--year",type=int, choices=range(2000,2020))
parser.add_argument("--site",type=str)
args = parser.parse_args()



# Drafts. Has been copied into use
# file = 'Data/dummy_file.csv' -> main()
# with open(file, 'r') as f: #opens csv file and reads is as a file ->  convert_dataset_into_titles_and_list_of_cases()
#     all_lines = f.readlines()
#     titles = all_lines.pop(0)   #removes first row of csv ans stores it in the list titles

class Case:
    def __init__(self, state, year, leading_site, sex, count):
        self.state = state
        self.year = year
        self.leading_site = leading_site
        self.sex = sex
        self.count = count
    
    def get_details(self): 
        return (f"State: {self.state}; Year: {self.year}; Leading Site: {self.leading_site}; Sex: {self.sex}; Count: {self.count}")
    
    def get_year(self):
        return self.year
    
    def get_leading_site(self):
        return self.leading_site
    
    def get_sex(self):
        return self.sex
    
    def get_count(self):
        return self.count
    
def split_data_string_to_list(string_with_commas):
        """Split a string read from the .csv file into a convenient list, so it can be indexed. 
        It also removes new line, if that's at the end of the last item.
        If the list is empty, return empty list"""
        try:
            split_entry = string_with_commas.split(",")
            #if split_entry[9][len(split_entry[9])-1] == "\n":
            split_entry[-1] = split_entry[-1].strip("\n")
        except IndexError:
            split_entry = []
        return split_entry

class CancerDataset: 
    def __init__(self, dataset_name):
        self.file = dataset_name # the .csv dataset file being accessed for the data
        self.list_of_cases = [] # list of cases, each of which is stored as a Case instance
    
    def convert_dataset_into_titles_and_list_of_cases(self):
        """opens the data file, and reads through each line of the file, outputting each to a list"""
        with open(self.file, 'r') as f: #opens csv file and reads it as a file
            all_lines = f.readlines() # get all the lines form the file
            return all_lines[0], all_lines[1:]   #removes first row of csv and returns it in the list titles
        
    
    
    def fill_list_of_cases(self):
        """adds individual Case instances to the list"""
        titles, raw_data = self.convert_dataset_into_titles_and_list_of_cases()
        for i in range(len(raw_data)):
            line_entry = split_data_string_to_list(raw_data[i])
            case_entry = Case(line_entry[2],line_entry[3],line_entry[5],line_entry[7],line_entry[9])
            self.list_of_cases.append(case_entry)

    # Note: Merge the below get_data_* methods into a single function to obey the Single Purpose Principle
    
    def get_data_from_year(self,year): 
        data_for_year = []
        for i in range(len(self.list_of_cases)): #for each Case
            if int(self.list_of_cases[i].get_year()) == year: #need to convert to an int first, since the year is stored as a string
                data_for_year.append(self.list_of_cases[i].get_details())
        return data_for_year
    
    def get_data_by_site(self,leading_site): 
        data_for_site = []
        for i in range(len(self.list_of_cases)): #for each Case
            if self.list_of_cases[i].get_leading_site() == leading_site:
                data_for_site.append(self.list_of_cases[i].get_details())
        return data_for_site

# example code
# case_example = Case("us", 2002, "mouth", "male", 2003)

file = 'Data/dummy_file.csv' #for now, just put a copy of dummy file in production code. Needs to be fixed!
dataset = CancerDataset(file) # now has a .list_of_cases = []
dataset.fill_list_of_cases() # now has a .list_of_cases = the whole file converted to list of Case instances
if args.site !=None:
    print(dataset.get_data_by_site(args.site))
if args.year !=None:
    print(dataset.get_data_from_year(args.year))



def main(): 
    #file = 'Data/dummy_file.csv'
    #dataset = CancerDataset(file) # now has a .list_of_cases = []
    #dataset.fill_list_of_cases() # now has a .list_of_cases = the whole file converted to list of Case instances
    pass

if __name__ == '__main__':
    main()