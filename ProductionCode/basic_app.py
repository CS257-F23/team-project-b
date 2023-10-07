from flask import Flask
from ProductionCode.watch import *

app = Flask(__name__)

@app.route('/year/<year_input>', strict_slashes=False)
def get_year(year_input):
    """Allows the user to input a year between 2000 and 2020, and get all the data from said year. 
    If they go to a year outside of this range, they'll be instructed what years they can access"""
    if year_input not in str(list(range(2000,2021))): #checks to see if input was valid, 
        #by quickly generating a list of years between 2000 and 2021, then converting to a string (so we can check with in function)
        return "That wasn't a valid input. Try sending a year between 2000 and 2020"
    return dataset.get_data_from_year(int(year_input))

@app.route('/site/<site_input>', strict_slashes=False)
def get_site(site_input):
    """Allows the user to input a cancer site from the list of availible options. If the user inputs the wrong option,
    they'll be taken to the homepage"""
    valid_options = ['Brain and Other Nervous System', 'Breast', 'Cervix Uteri', 'Colon and Rectum', 'Corpus Uteri', 'Esophagus', 'Gallbladder', 'Kidney and Renal Pelvis', 'Larynx', 'Leukemias', 'Liver', 'Lung and Bronchus', 'Melanoma of the Skin', 'Myeloma', 'Non-Hodgkin Lymphoma', 'Oral Cavity and Pharynx', 'Ovary', 'Pancreas', 'Prostate', 'Stomach', 'Thyroid', 'Urinary Bladder invasive and in situ']
    if site_input not in valid_options:
        return "That's not a valid input; please try again! <br/> <br/> the valid options are: " + str(valid_options).strip("[]") #removing brackets from list, because they're ugly
    return dataset.get_data_by_site(site_input)    

@app.route('/')
def homepage():
    """a simple homepage, with information about how to use, and some examples"""
    homestring = """Welcome to Marshall's 2nd Individual Deliverable: 
    <br/> <br/> To use the website, add /year/ or /site/ to the url, followed by the parameter of interest.
    <br/> <br/> For /year/ valid choices are any year between 2000 and 2020
    <br/> <br/> For /site/, valid choices include: 'Brain and Other Nervous System', 'Breast', 'Cervix Uteri', 'Colon and Rectum', 'Corpus Uteri', 'Esophagus', 'Gallbladder', 'Kidney and Renal Pelvis', 'Larynx', 'Leukemias', 'Liver', 'Lung and Bronchus', 'Melanoma of the Skin', 'Myeloma', 'Non-Hodgkin Lymphoma', 'Oral Cavity and Pharynx', 'Ovary', 'Pancreas', 'Prostate', 'Stomach', 'Thyroid', 'Urinary Bladder invasive and in situ' 
    <br/> <b>(case sensitive)</b>
    <br/> <br/> <br/> For example, try navigating to 127.0.0.1:5000/year/2007 or 127.0.0.1:5000/site/Cervix Uteri""" 
    #referenced campuswire for the neat <br/> trick
    return homestring

if __name__ == '__main__':
    app.run()