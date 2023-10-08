from flask import Flask, render_template
from ProductionCode.watch import *

def load_data():
    """Create the global 'dataset' variable to used in later functions."""
    global dataset
    file = 'Data/clean_incidence.csv' #for now, just put a copy of dummy file in production code. Needs to be fixed!
    dataset = CancerDataset(file) # now has a .list_of_cases = []
    dataset.fill_list_of_cases() # now has a .list_of_cases = the whole file converted to list of Case instances

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