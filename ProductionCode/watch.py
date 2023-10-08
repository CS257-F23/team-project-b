"""
A simple command line program that provides the user with data from the cdc US cancer database from 2000-2020. 
To use, send "python3 /ProductionCode/watch.py --(argument) --(data of interest)
Currently, two arguments are supported:
--year (year between 2000-2020)
--site '(site)'
*must choose from list of availible sites. to see which are availible, try using the -h command.
Important links:
https://docs.python.org/3/library/csv.html
https://anyaevostinar.github.io/classes/257-f23/project-command-line
"""

import csv
import argparse

class Case:
    """An object that represents an individual line of the data file. Contains the total number of individuals with cancer for 
    each unique combination of state,year,cancer-site, and gender."""
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
        split_entry = string_with_commas.split(",")
        #if split_entry[9][len(split_entry[9])-1] == "\n":
        split_entry[-1] = split_entry[-1].strip("\n")
        return split_entry

class CancerDataset: 
    """A class that contains each case (line) from the full data set. """
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
        for i in range(len(raw_data)):  #POSSIBLY CHANGE TO
                                        # for case in raw_data
            line_entry = split_data_string_to_list(raw_data[i])
            case_entry = Case(line_entry[1],line_entry[4],line_entry[5],line_entry[7],line_entry[9])
            self.list_of_cases.append(case_entry)

    # Note: Merge the below get_data_* methods into a single function to obey the Single Purpose Principle
    
    def get_data_from_year(self,year): 
        """given a valid input year, returns a list of all cases associated with that year"""
        data_for_year = []
        for i in range(len(self.list_of_cases)): #for each Case
            if int(self.list_of_cases[i].get_year()) == year: #need to convert to an int first, since the year is stored as a string
                data_for_year.append(self.list_of_cases[i].get_details())
        return data_for_year
    
    def get_data_by_site(self,leading_site): 
        """given a valid input cancer site, returns a list of all cases associated with that site"""
        data_for_site = []
        for i in range(len(self.list_of_cases)): #for each Case
            if self.list_of_cases[i].get_leading_site() == leading_site:
                data_for_site.append(self.list_of_cases[i].get_details())
        return data_for_site

    def get_total_for_site(self,leading_site):
        """calculates and returns the total number of cancer incidinces for a given site between the years 2000-2020"""
        total_cases = 0
        for case in self.list_of_cases:
            if case.get_leading_site() == leading_site:
                total_cases += int(case.get_count())  
        return total_cases

def parse_commandline_args():
    """checks to see what arguments the user has given, and displays it."""
    if args.site !=None:
        return (dataset.get_data_by_site(args.site))
    if args.year !=None:
        return (dataset.get_data_from_year(args.year))

def make_primary_dataset_instance():
    """Creates an instance of the primary dataset file. (primary = initial dataset from CDC; not supplementary, like mortality, race etc)"""
    #file = 'Data/dummy_file.csv'
    file = 'Data/clean_incidence.csv' #for now, just put a copy of dummy file in production code. Needs to be fixed!
    dataset = CancerDataset(file) # now has a .list_of_cases = []
    dataset.fill_list_of_cases() # now has a .list_of_cases = the whole file converted to list of Case instances
    return dataset

dataset = make_primary_dataset_instance() #make a dataset file for all the functions to call.

def main(): 
    print(parse_commandline_args())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple program that allows a user to access cancer data. To use, try using --year (a year between 2000-2000) or --site '(a cancer site)'. To see availible sites, try sending -h' ")
    #referenced realPython tutorial for CLI implementation.
    parser.add_argument("--year",type=int, choices=range(2000,2021))
    parser.add_argument("--site",type=str, choices=['Brain and Other Nervous System', 'Breast', 'Cervix Uteri', 'Colon and Rectum', 'Corpus Uteri', 'Esophagus', 'Gallbladder', 'Kidney and Renal Pelvis', 'Larynx', 'Leukemias', 'Liver', 'Lung and Bronchus', 'Melanoma of the Skin', 'Myeloma', 'Non-Hodgkin Lymphoma', 'Oral Cavity and Pharynx', 'Ovary', 'Pancreas', 'Prostate', 'Stomach', 'Thyroid', 'Urinary Bladder invasive and in situ'])
    args = parser.parse_args()
    main()
