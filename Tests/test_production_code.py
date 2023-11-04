"""
A collection of tests for the watch.py program. To run, navigate to /team-project-b/ and send 'python3 -m unittest discover Tests/' """
import unittest
from Data import *
from Data.datasource import *
from cl import *
import subprocess

def setUp():
    global database
    database = DataSource()

  

if __name__ == '__main__':
    unittest.main()
