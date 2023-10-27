import psycopg2
import ProductionCode.psqlConfig as config

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
    
    def get_total_and_details(self,target_datas:list):
        command_for_sql = construct_multiargument_query(target_datas)
        cursor = self.connection.cursor()
        cursor.execute(command_for_sql)
        result = cursor.fetchall()
        return result

    def return_sorted_state(self,state):
        """returns a list of the contents of each row with the specified date. For convenience, this list is sorted by the year of occurrence."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM cancerData WHERE state_name=%s ORDER BY case_year", (state,))
        result = cursor.fetchall()
        return result
    
    

    
def construct_multiargument_query(target_datas:list):
    """Returns an sql command which will fetch all data that matches the arguments of interest (target_datas)"""
    sql_command = "SELECT * FROM cancerData WHERE "
    for argument in target_datas:
       arg_type = identify_argument(argument)
       if arg_type != None:
            sql_command = sql_command + arg_type + " = " + str(argument) + " "
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
