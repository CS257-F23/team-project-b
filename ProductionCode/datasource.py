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
        """returns the total number of cases (between 2000-2020) of any type of cancer in a given state"""
        command_for_sql = "SELECT SUM(case_count) FROM cancerData WHERE state_name = '"+ str(state) + "';"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result[0][0]
    
    def get_ranked_list_for_state(self,state):
        """gets the top 10 most prevalent cancer types from the last 20 years (for men and women) for a given state
        referenced: https://www.w3resource.com/sql/aggregate-functions/sum-function.php for SUM() and GROUP BY functionality"""
        command_for_sql = "SELECT leading_site, SUM(case_count) FROM cancerData WHERE state_name = '" + str(state) + "' GROUP BY leading_site ORDER BY SUM(case_count) DESC LIMIT 10;"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result
    
    def get_total_for_site(self, leading_site):
        """returns the total cancer cases for a given cancer site between the years 2000-2020"""
        command_for_sql = "SELECT SUM(case_count) FROM cancerData WHERE leading_site = '"+ str(leading_site) + "'"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result[0][0]
    
    def get_total_for_year(self, year):
        """returns the total number of cancer cases in a given year"""
        command_for_sql = "SELECT SUM(case_count) FROM cancerData WHERE case_year = '"+ str(year)+"'"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result[0][0]
    
    def get_data_by_site(self, site):
        """returns all the data for a given site"""
        command_for_sql = "SELECT * FROM cancerData WHERE leading_site = '" + \
            str(site) + "'"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result
    
    def get_data_from_year(self, year):
        """returns all the data from a given year"""
        command_for_sql = "SELECT * FROM cancerData WHERE case_year = '" + \
            str(year) + "'"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result
    
    def run_sql_command_and_return_result(self,command_for_sql:str):
        cursor = self.connection.cursor()
        cursor.execute(command_for_sql)
        result = cursor.fetchall()
        return result
    
    #potentially move parse_URL_string_to_list to a new watch.py file; don't know where else it would fit. Also, refactor the sort out function below
    
    def get_total_for_year_and_site(self, year, leading_site):
        """Given a year and site value, returns the total number of cancer cases"""
        command_for_sql = "SELECT SUM(case_count) FROM cancerData WHERE case_year = '"+ str(year)+"' AND leading_site = '"+ str(leading_site) + "'"
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result[0][0]

    
    def get_ranked_list_by_year_and_site(self,year,site):
        """returns a dictionary containing ranked top 10 lists (for each sex) of cancer cases in the given year and site"""
        command_for_flist = "SELECT state_name, case_count FROM cancerData WHERE sex = 'Female' AND case_year = '" + str(year) + "' AND leading_site = '" + str(site) + "'ORDER BY case_count DESC LIMIT 10"
        command_for_mlist = "SELECT state_name, case_count FROM cancerData WHERE sex = 'Male' AND case_year = '" + str(year) + "' AND leading_site = '" + str(site) + "'ORDER BY case_count DESC LIMIT 10"
        flist = self.run_sql_command_and_return_result(command_for_flist)
        mlist = self.run_sql_command_and_return_result(command_for_mlist)
        output = {"Male top ten list": mlist, "Female top ten list" : flist}
        return output

    def return_sorted_state(self,state):
        """returns a list of the contents of each row with the specified date. For convenience, this list is sorted by the year of occurrence."""
        command_for_sql = "SELECT * FROM cancerData WHERE state_name=%s ORDER BY case_year", (state,)
        result = self.run_sql_command_and_return_result(command_for_sql)
        return result
    
    def return_variable_arguments_query_result(self, combination_method:str, target_datas:list):
        """Sort target_datas into invalid targets and valid targets (which will be accompanied with their column of appearance)
        Extract valid targets into its own list for display in the website with the invalid targets
        Create relevant SQL commands, run them and get the resultant subset of the table
        Craft the dictionary used in app.py for rendering"""
        invalid_query_parameters, valid_column_and_query_parameters = sort_out_invalid_and_valid_query_parameters_with_column(target_datas)
        valid_query_parameters = []
        valid_query_parameters = [parameter for _,parameter in valid_column_and_query_parameters if parameter not in valid_query_parameters]
        command_for_get_all_cases = construct_multiargument_query_target_all(combination_method, valid_column_and_query_parameters)
        command_for_get_total_case_counts = command_for_get_all_cases.replace("*", "SUM(case_count)")
        all_cases = self.run_sql_command_and_return_result(command_for_get_all_cases)
        total_count = self.run_sql_command_and_return_result(command_for_get_total_case_counts) # Take the form of a list of 1 tuple like: [(15328977,)]
        total_count = total_count[0][0]
        
        # Craft the output to be rendered into the Template
        return {
            'total count': total_count,
            'valid input': valid_query_parameters,
            'invalid input': invalid_query_parameters,
            'subset': all_cases
        }
        
def sort_out_invalid_and_valid_query_parameters_with_column(query_parameters:list):
    """
    Find which query parameter is a valid one for filtering, and if so add the column name. If not valid, add it to a separate list.
    Example:
    From query_parameters such as ["Texas","Male","Liver","Dead"], split it into:
    valid_query_parameters = [["state_name","Texas"], ["sex","Male"], ["leading_site","Liver"]]
    invalid_query_parameters = ["Dead"]
    """
    invalid_query_parameters = []
    valid_column_and_query_parameters = []
    for argument in query_parameters:
        target_column = find_column_containing(argument)
        if target_column == 'invalid' and argument not in invalid_query_parameters:
            invalid_query_parameters.append(argument)
        else:
            column_and_argument = [target_column, argument]
            valid_column_and_query_parameters.append(column_and_argument)
    return invalid_query_parameters, valid_column_and_query_parameters

#TODO refactor this:
def construct_multiargument_query_target_all(combination_method:str, valid_columns_and_arguments:list):
    """Returns an sql command which will fetch all data that matches the arguments of interest
    combination_method can only be 'and' or 'or', and will be changed to 'AND' and 'OR'
    Example of valid_columns_and_arguments: [["state_name","Texas"], ["sex","Male"], ["leading_site","Liver"]]
    Example of output: SELECT * FROM cancerData WHERE state_name = 'Texas' AND sex = 'Male' AND leading_site = 'Liver'
    """
    combination_method = combination_method.upper()
    sql_command = "SELECT * FROM cancerData WHERE"
    for column_and_argument in valid_columns_and_arguments:
       target_column = column_and_argument[0]
       target_data = column_and_argument[1]
       sql_command = f"{sql_command} {target_column} = '{target_data}' {combination_method}"
    last_char_in_command = sql_command[-1] # Whittle down the command until the closing excess command word is removed
    while last_char_in_command != " ":
        sql_command = sql_command[:-1] 
        last_char_in_command = sql_command[-1]
    sql_command += ";" # Add the closing semicolon
    return sql_command

def construct_multiargument_query_specified_targets(combination_method:str, targets_to_return:list,valid_columns_and_arguments:list):
    """Creates an SQL command which has specified targets (rather than just *) given a list of targets, and a list of query parameters. 
    Both args should be lists of strings.
    Works by running construct_multiargument_query_target_all with valid_columns_and_arguments and replace '*' with the targets_to_return"""
    sql_command = construct_multiargument_query_target_all(combination_method, valid_columns_and_arguments)
    targets_as_string = ""
    for target in targets_to_return:
        targets_as_string = targets_as_string + str(target) + ", "
    targets_as_string = targets_as_string[:-2] # Remove trailing comma and whitespace
    sql_command = sql_command.replace("*",targets_as_string)
    return sql_command
    
def find_column_containing(argument:str):
    """given an argument (ie: '2003', 'Liver', or 'Female') and returns the appropriate column that corresponds to the field."""
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
