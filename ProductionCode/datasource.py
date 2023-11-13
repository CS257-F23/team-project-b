import psycopg2
import Data.psqlConfig as config

class DataSource:

    def __init__(self):
        '''Constructor that initiates connection to database'''
        self.connection = self.connect()

    def connect(self):
        '''Initiates connection to database using information in the psqlConfig.py file.
        Returns the connection object.'''

        try:
            connection = psycopg2.connect(database=config.database, user=config.user, host="localhost",password = config.password)
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection
    
    def get_total_for_state(self,state):
        """returns the total number of cases (between 2000-2020) of any type of cancer in a given state
        Params: state - a string corresponding to name of state
        Returns: an int corresponding to the number of total cancer cases between 2000-2020 """
        command_for_sql = "SELECT SUM(case_count) FROM cancerData WHERE state_name = '"+ str(state) + "';"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result[0][0]
    
    def get_ranked_list_for_state(self,state):
        """gets the top 10 most prevalent cancer types from the last 20 years (for men and women) for a given state
        referenced: https://www.w3resource.com/sql/aggregate-functions/sum-function.php for SUM() and GROUP BY functionality
        Params: state - a string corresponding to the name of state
        Returns: a list containing tuples. Each tuple contains the site name followed by the number of cases associated with that site"""
        command_for_sql = "SELECT leading_site, SUM(case_count) FROM cancerData WHERE state_name = '" + str(state) + "' GROUP BY leading_site ORDER BY SUM(case_count) DESC LIMIT 10;"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result
    
    def get_total_for_site(self, leading_site):
        """returns the total cancer cases for a given cancer site between the years 2000-2020
        Params: leading_site - a string corresponding to the name of the cancer site
        Returns: an int corresponding to the nummber of  cases associated with the leading site"""
        command_for_sql = "SELECT SUM(case_count) FROM cancerData WHERE leading_site = '"+ str(leading_site) + "'"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result[0][0]
    
    def get_total_for_year(self, year):
        """returns the total number of cancer cases in a given year
        Params: year - an int corresponding to a year between 2000-2020
        Returns: an int correspoding to the total number of cancer cases in a given year"""
        command_for_sql = "SELECT SUM(case_count) FROM cancerData WHERE case_year = '"+ str(year)+"'"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result[0][0]
    
    def get_data_by_site(self, site):
        """returns all the data for a given site
        Params: site - a string corresponding to the cancer site of interest
        Returns: a list of tuples, where each tuple contains the state, year, site, sex, and count"""
        command_for_sql = "SELECT * FROM cancerData WHERE leading_site = '" + \
            str(site) + "'"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result
    
    def get_data_from_year(self, year):
        """returns all the data from a given year
        Params: year - an int corresponding to the site of interest
        Returns: a list of tuples, where each tuple contains the state, year, site, sex, and count"""
        command_for_sql = "SELECT * FROM cancerData WHERE case_year = '" + \
            str(year) + "'"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result
    
    def get_simple_search_data(self, input_targets:list):
        """Called by simple search page; returns the total number of cases associated with a user's search
        Params: input_targets - a list of valid parameters that the user has input (ie: ["Texas",2005,"Liver"])
        Returns: an int corresponding to the number of cancer cases that match the user input"""
        sql_command = construct_multiargument_query_specified_targets(["SUM(case_count)"], input_targets)
        number_of_matches = self.run_sql_command_and_return_result(sql_command)
        number_of_matches = number_of_matches[0][0] # Extract from [(3,)] to 3
        return number_of_matches
    
    def run_sql_command_and_return_result(self,command_for_sql:str):
        """Runs an sql command and returns the result
        Params: command_for_sql - a string which will be sent to the SQL database
        Retruns: the output directly from sql (depending on method, outputs either list, int, or string)"""
        cursor = self.connection.cursor()
        cursor.execute(command_for_sql)
        result = cursor.fetchall()
        return result

def construct_multiargument_query_target_all(valid_arguments:list):
    """Returns an sql command which will fetch all data (*) that matches the arguments of interest
    Params: valid_arguments - a list of strings, where each string is a parameter that the user inputs
    Returns: a string which can be directly input into sql
    """
    sql_command = "SELECT * FROM cancerData WHERE"
    for argument in valid_arguments:
       sql_command = f"{sql_command} {find_column_containing(argument)} = '{argument}' AND"
    last_char_in_command = sql_command[-1] # Whittle down the command until the closing excess command word ('AND' or 'WHERE') is removed
    while (last_char_in_command) != " ":
        sql_command = sql_command[:-1] 
        last_char_in_command = sql_command[-1]
    sql_command += ";" # Add the closing semicolon
    return sql_command

def construct_multiargument_query_specified_targets(targets_to_return:list,valid_arguments:list):
    """Creates an SQL command which has specified targets (rather than just *) given a list of targets, and a list of query parameters. 
    Both args should be lists of strings.
    Params: targets_to_return - a list of strings containing the data that sql should return
            valid_arguments - a list of strings containing the arguments which sql should sort by (aka the values that come after WHERE)
    Works by running construct_multiargument_query_target_all with valid_columns_and_arguments and replace '*' with the targets_to_return"""
    sql_command = construct_multiargument_query_target_all(valid_arguments)
    targets_as_string = ""
    for target in targets_to_return:
        targets_as_string = targets_as_string + str(target) + ", "
    targets_as_string = targets_as_string[:-2] # Remove trailing comma and whitespace
    sql_command = sql_command.replace("*",targets_as_string)
    return sql_command

def find_column_containing(argument:str):
    """given an argument (ie: '2003', 'Liver', or 'Female') and returns the appropriate column that corresponds to the field.
    Params: argument - a string corresponding to a specific argument value
    Returns: a string related to the name of the column that the input data can be found in. Can either be 'state_name', 'case_year', 'leading_site', 'sex' or 'invalid' """
    possible_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                       'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    possible_years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
                      2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    possible_years = [str(year) for year in possible_years]

    possible_leading_sites = ['Brain and Other Nervous System', 'Breast', 'Cervix Uteri', 'Colon and Rectum', 'Corpus Uteri', 'Esophagus', 'Gallbladder', 'Kidney and Renal Pelvis', 'Larynx', 'Leukemias', 'Liver',
                                'Lung and Bronchus', 'Melanoma of the Skin', 'Myeloma', 'Non-Hodgkin Lymphoma', 'Oral Cavity and Pharynx', 'Ovary', 'Pancreas', 'Prostate', 'Stomach', 'Thyroid', 'Urinary Bladder invasive and in situ']

    possible_sexes = ['Female', 'Male']
    
    target_column = "invalid"
    if argument in possible_states:
        target_column = 'state_name'
    elif argument in possible_years:
        target_column = 'case_year'
    elif argument in possible_leading_sites:
        target_column = 'leading_site'
    elif argument in possible_sexes:
        target_column = 'sex'
    
    return target_column
