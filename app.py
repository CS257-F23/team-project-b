from flask import Flask, render_template
from ProductionCode.watch import *

def load_data():
    """Create the global 'dataset' variable to used in later functions."""
    global dataset
    file = 'Data/clean_incidence.csv' #for now, just put a copy of dummy file in production code. Needs to be fixed!
    dataset = CancerDataset(file) # now has a .list_of_cases = the whole file converted to list of Case instances

def parse_URL_string_to_list(URL_string_input):
    """Helper function to get_filtered_data. Convert inputs like 'Liver,%202007' from the URL into ['Liver', '2007'] for uses in the method get_total_and_details in watch.py."""
    proper_whitespace_string = URL_string_input.replace("%20", " ")
    separated_target_data = proper_whitespace_string.split(",")
    list_of_target_data = list(separated_target_data)
    striped_list_of_target_data = [data.strip() for data in list_of_target_data]
    return striped_list_of_target_data

app = Flask(__name__)

@app.route('/')
def homepage():
    """The homepage, giving an introduction to the Flask webpages and how to navigate it with the URL."""
    return render_template("home_page.html", title = "Home Page")

@app.route('/year/<year_argument>', strict_slashes=False)
def get_year_data(year_argument):
    """From the URL input, run the imported production method to fetch the details in the form of a list, then make it presentable. For unavailable URL, return the error message."""
    filtered_data = dataset.get_data_from_year(int(year_argument))
    if filtered_data == []: return render_template("error_message.html", title = "Error!", message = "The year that you have entered is invalid.")
    else: return render_template("subset_display.html", title = "Year subset", field = "year", data = year_argument, subset = filtered_data, total_count = dataset.get_total_for_year(year_argument))

@app.route('/site/<site_argument>', strict_slashes=False)
def get_site_data(site_argument):
    """From the URL input, run the imported production method to fetch the details in the form of a list, then make it presentable. For unavailable URL, return the error message."""
    filtered_data = (dataset.get_data_by_site(site_argument))
    if filtered_data == []: return render_template("error_message.html", title = "Error!", message = "The leading site that you have entered is invalid.")
    else: return render_template("subset_display.html", title = "Site subset", field = "leading site", data = site_argument, subset = filtered_data, total_count = dataset.get_total_for_site(site_argument))

@app.route('/<combination_method>/<target_datas>', strict_slashes=False)
def get_filtered_data(combination_method, target_datas):
    """From the URL input, run the imported production method to fetch the details in the form of a dictionary consisting of: 
        - 'total count': The total [count] of all matched Cases
        - 'valid input': Which target_data has found matched Cases
        - 'invalid input': Which target_data has NOT found matched Cases
        - 'case details': Listing out the details of all matched Cases
    For unavailable URL, return the error message."""
    filtered_data = dataset.get_total_and_details(combination_method, parse_URL_string_to_list(target_datas))
    if filtered_data["total count"] == 0: return render_template("error_message.html", title = "Error!", message = "The input that you have entered has no matching cases.")
    else: return render_template("information_display.html", title = "Site subset", total_count = filtered_data['total count'], valid_input = filtered_data['valid input'], invalid_input = filtered_data['invalid input'], subset = filtered_data['case details'])
    
@app.errorhandler(404)
def page_not_found(e):
    """For when 404 error is encountered, such that a potentially possible but non-existant URL is used such as /year/4444."""
    return render_template("error_message.html", title = "Error!", message = "The URL that you have entered is invalid.")

@app.errorhandler(500)
def python_bug(e):
    """For when a runtime error is encountered in the code itself."""
    return render_template("error_message.html", title = "Error!", message = "It seems that a bug has occurred in the codes.")


if __name__ == '__main__':
    load_data()
    app.run()