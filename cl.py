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

from ProductionCode.watch import *
import argparse
from Data.datasource import *
#import sys
#import os
#sys.path.append("ProductionCode")


def parse_commandline_args(args, dataset):
    """checks to see what arguments the user has given, and displays it. takes args, a Namespace containing args for year and site, and a CancerData object"""
    if args.site != None:
        # added total for revision of CLI
        return (str(database.get_data_by_site(args.site))+"\ntotal cases: "+str(database.get_total_for_site(args.site)))
    if args.year != None:
        return (str(database.get_data_from_year(args.year))+"\ntotal cases: "+str(database.get_total_for_year(args.year)))
    else:  # if the user enters no arguments, they'll get a helpful statement telling them how to proceed!
        print("\n------Welcome to the WATCH app------ \n \nTo use via command line, try sending --year or --site, followed by the information of interest. \n \nFor more information, please consult the readme. You can also run --help to see valid arguments for each command")
        return ""  # returns empty string to avoid printing of 'None'


def main():
    #global dataset
    #dataset = CancerDataset("Data/clean_incidence.csv")
    global database
    database = DataSource()
    # print(dataset.get_total_for_year_and_site(
    #    2000, "Liver"))  # Example code for testing
    print(parse_commandline_args(args, dataset))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple program that allows a user to access cancer data. To use, try using --year (a year between 2000-2000) or --site '(a cancer site)'. To see availible sites, try sending -h' ")
    # referenced realPython tutorial for CLI implementation.
    parser.add_argument("--year", type=int, choices=range(2000, 2021))
    parser.add_argument("--site", type=str, choices=['Brain and Other Nervous System', 'Breast', 'Cervix Uteri', 'Colon and Rectum', 'Corpus Uteri', 'Esophagus', 'Gallbladder', 'Kidney and Renal Pelvis', 'Larynx', 'Leukemias',
                        'Liver', 'Lung and Bronchus', 'Melanoma of the Skin', 'Myeloma', 'Non-Hodgkin Lymphoma', 'Oral Cavity and Pharynx', 'Ovary', 'Pancreas', 'Prostate', 'Stomach', 'Thyroid', 'Urinary Bladder invasive and in situ'])
    args = parser.parse_args()
    main()
