"""
A simple command line program that provides the user with data from the cdc US cancer database from 2000-2020.
To use, send "python3 cl.py --(argument) --(data of interest)
Currently, two arguments are supported:
--year (year between 2000-2020)
--site '(site)'
*must choose from list of availible sites. to see which are availible, try using the -h command.
Important links:
https://docs.python.org/3/library/csv.html
https://anyaevostinar.github.io/classes/257-f23/project-command-line
"""

import argparse
from ProductionCode.datasource import *

def parse_commandline_args(args):
    """checks to see what arguments the user has given, and displays it. takes args, a Namespace containing args for year and site, and a CancerData object
    Params: args - a namespace containing fields for site and year aswell as the user's arguments (if they provided one for the given field)
    Returns: a string containing either the data the user was interested in, or a help statement to guide the user on how to use the app via command line."""
    if args.site != None:
        return get_formatted_site_output(args.site)
    if args.year != None:
        return get_formatted_year_output(args.year)
    else:  
        return display_usage_info()

def get_formatted_site_output(site:str):
    """returns formatted data from the sql database for the command line
    Params: site - a string corresponding to the cancer site 
    Returns: a string containing all the database's data related to that site aswell as the total number of cases of that site"""
    total_data = database.get_data_by_site(site)
    total_cases = database.get_total_for_site(site)
    output_str = str(total_data) + "\ntotal cases: " + str(total_cases)
    return output_str

def get_formatted_year_output(year):
    """returns formatted data from the sql database for the command line
    Params: year - an int corresponding to the cancer site 
    Returns: a string containing all the database's data related to that site aswell as the total number of cases of that site"""
    total_data = database.get_data_from_year(year)
    total_cases = database.get_total_for_year(year)
    output_str = str(total_data) + "\ntotal cases: " + str(total_cases)
    return output_str 

def display_usage_info():
    """A simple function that stores the usage information so it can be easily printed
    Params:
    Returns: an empty string, so a none object isn't randomly printed to command line"""
    print("\n------Welcome to the WATCH app------ \n \nTo use via command line, try sending --year or --site, followed by the information of interest. \n \nFor more information, please consult the readme. You can also run --help to see valid arguments for each command")
    return ""  

def main():
    global database
    database = DataSource()
    print(parse_commandline_args(args))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple program that allows a user to access cancer data. To use, try using --year (a year between 2000-2000) or --site '(a cancer site)'. To see availible sites, try sending -h' ")
    # referenced realPython tutorial for CLI implementation.
    parser.add_argument("--year", type=int, choices=range(2000, 2021))
    parser.add_argument("--site", type=str, choices=['Brain and Other Nervous System', 'Breast', 'Cervix Uteri', 'Colon and Rectum', 'Corpus Uteri', 'Esophagus', 'Gallbladder', 'Kidney and Renal Pelvis', 'Larynx', 'Leukemias',
                        'Liver', 'Lung and Bronchus', 'Melanoma of the Skin', 'Myeloma', 'Non-Hodgkin Lymphoma', 'Oral Cavity and Pharynx', 'Ovary', 'Pancreas', 'Prostate', 'Stomach', 'Thyroid', 'Urinary Bladder invasive and in situ'])
    args = parser.parse_args()
    main()
