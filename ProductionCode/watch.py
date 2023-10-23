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
from ProductionCode.cancerDataset_obj import *


def main():
    global dataset
    dataset = CancerDataset("Data/clean_incidence.csv")


if __name__ == "__main__":
    main()
