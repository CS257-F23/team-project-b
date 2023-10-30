"""A program that creates an instance of the CDC 2000-2020 dataset file for use with other parts of 
the WATCH website project."""

import csv
from ProductionCode.cancerDataset_obj import *

def main():
    global dataset
    dataset = CancerDataset("Data/clean_incidence.csv")

if __name__ == "__main__":
    main()
