import psycopg2
import psqlConfig as config

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
    
    def get_data_from_year(self, year):
        """Docstring"""
        command_for_sql = "SELECT * FROM cancerData WHERE case_year = '" + \
            str(year) + "'"
        cursor = self.connection.cursor()
        cursor.execute(command_for_sql)
        result = cursor.fetchall()
        return result

    def get_data_by_site(self, site):
        """Docstring"""
        command_for_sql = "SELECT * FROM cancerData WHERE leading_site = '" + \
            str(site) + "'"
        cursor = self.connection.cursor()
        cursor.execute(command_for_sql)
        result = cursor.fetchall()
        return result
    
    def get_total_for_site(self, leading_site):
        """Docstring"""
        command_for_sql = "SELECT SUM(case_count) FROM cancerData WHERE leading_site = '"+ str(leading_site) + "'"
        cursor = self.connection.cursor()
        cursor.execute(command_for_sql)
        result = cursor.fetchall()
        return result

    
    def get_total_and_details(self,target_datas:list):
        command_for_sql = construct_multiargument_query_target_all(target_datas)
        cursor = self.connection.cursor()
        cursor.execute(command_for_sql)
        result = cursor.fetchall()
        return result
    
   

    
    def get_ranked_list_by_year_and_site(self,year,site):
        """returns a dictionary containing ranked top 10 lists (for each sex) of cancer cases in the given year and site"""
        command_for_flist = "SELECT state_name, case_count FROM cancerData WHERE sex = 'Female' AND case_year = '" + str(year) + "' AND leading_site = '" + str(site) + "'ORDER BY case_count DESC LIMIT 10"
        command_for_mlist = "SELECT state_name, case_count FROM cancerData WHERE sex = 'Male' AND case_year = '" + str(year) + "' AND leading_site = '" + str(site) + "'ORDER BY case_count DESC LIMIT 10"
        cursor = self.connection.cursor()
        cursor.execute(command_for_flist)
        flist = cursor.fetchall()
        cursor.execute(command_for_mlist)
        mlist = cursor.fetchall()
        output = {"Male top ten list": mlist, "Female top ten list" : flist}
        return output

    def return_sorted_state(self,state):
        """returns a list of the contents of each row with the specified date. For convenience, this list is sorted by the year of occurrence."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM cancerData WHERE state_name=%s ORDER BY case_year", (state,))
        result = cursor.fetchall()
        return result
    
    
def construct_multiargument_query_target_all(query_parameters:list):
    """Returns an sql command which will fetch all data that matches the arguments of interest (query_parameters)"""
    sql_command = "SELECT * FROM cancerData WHERE "
    for argument in query_parameters:
       arg_type = identify_argument(argument)
       if arg_type != None:
            sql_command = sql_command + arg_type + "= '" + str(argument) + "' AND "
    sql_command = sql_command[:-4] #removes the last " AND" from the command
    return sql_command

def construct_multiargument_query_specified_targets(targets_to_return:list,query_parameters:list):
    """Creates an SQL command which has specified targets (rather than just *) given a list of targets, and a list of query parameters. 
    Both args should be lists of strings"""
    sql_command = construct_multiargument_query_target_all(query_parameters)
    targets_as_string = ""
    for target in targets_to_return:
        targets_as_string = targets_as_string + str(target) + ", "
    targets_as_string = targets_as_string[:-2]
    sql_command = sql_command.replace("*",targets_as_string)
    return sql_command

    
def identify_argument(argument:str):
    """given an argument (ie: 2003, Liver, Female) and returns the appropriate column that corresponds to the field."""
    possible_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                       'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    possible_years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
                      2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    possible_years = [str(year) for year in possible_years]

    possible_leading_sites = ['Brain and Other Nervous System', 'Breast', 'Cervix Uteri', 'Colon and Rectum', 'Corpus Uteri', 'Esophagus', 'Gallbladder', 'Kidney and Renal Pelvis', 'Larynx', 'Leukemias', 'Liver',
                                'Lung and Bronchus', 'Melanoma of the Skin', 'Myeloma', 'Non-Hodgkin Lymphoma', 'Oral Cavity and Pharynx', 'Ovary', 'Pancreas', 'Prostate', 'Stomach', 'Thyroid', 'Urinary Bladder invasive and in situ']

    possible_sexes = ['Female', 'Male']
    if argument in possible_states:
        return 'state_name'
    elif argument in possible_years:
        return 'case_year'
    elif argument in possible_leading_sites:
        return 'leading_site'
    elif argument in possible_sexes:
        return 'sex'
    else:
        return None

testSource = DataSource()
#print(testSource.get_total_and_details(["Maine","Liver", "Female", "2004"]))
#print(testSource.get_ranked_list_by_year_and_site("2002","Breast"))
print(construct_multiargument_query_specified_targets(["case_year","sex"],["2002","Liver"]))