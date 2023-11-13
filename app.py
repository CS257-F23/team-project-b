import io

# Flask imports
from flask import Flask, render_template, request, Response
from ProductionCode.datasource import *


def load_data():
    """Create the global 'dataset' variable to used in later functions.
    Params: None
    Returns: None"""
    global database
    database = DataSource()  # from sql


def get_args_from_form(list_of_args):
    """A helper function that grabs the input from a form given a list of form value names
    Params: list_of_args - a list of strings (each string is the id value from an html form)
    Returns: a list of user inputs corresponding to each value in list_of_args"""
    output_list = []
    for arg in list_of_args:
        if request.method == "POST":
            output_list.append(request.form[arg])
        elif request.method == "GET":
            output_list.append(request.args[arg])
    return output_list


app = Flask(__name__)


@app.route('/stateinfo', methods=['GET', 'POST'])
def state_info_display():
    """a display page for information by state
    Params: None
    Returns: rendering of state_info_display.html"""
    target_state = get_args_from_form(["state_for_info_page"])[0]
    total_incidences = database.get_total_for_state(target_state)
    most_common_cancers_list = database.get_ranked_list_for_state(target_state)
    return render_template("state_info_display.html", title="state info", total_count=total_incidences, state_choice=target_state, list_of_cancers=most_common_cancers_list)


@app.route('/simpsearch', strict_slashes=False, methods=['GET', 'POST'])
def display_number_of_matches(number_of_matches=0):
    """Filter the dataset by 4 input and return the result to be displayed.
    Input includes a State, Year, Site, and Sex, all can either be specified for left as 'Any'
    Params: number of matches (determined by user input in form)
    Returns: rendering of simple_search.html
    """
    try:  # When accessed using in-page Submit
        target_list = get_args_from_form(["state", "year", "site", "sex"])
    except:  # When accessed with nav bar
        target_list = ["", "", "", ""]
    while "" in target_list:
        target_list.remove("")
    number_of_matches = database.get_simple_search_data(target_list)
    return render_template("simple_search.html", title="Simple Search", number_of_matches=number_of_matches, target_list=target_list)


@app.route('/year/<year_argument>', strict_slashes=False)
def get_year_data(year_argument):
    """From the URL input, run the imported production method to fetch the details in the form of a list, then make it presentable. For unavailable URL, return the error message.
    Params: year_argument - a string supplied in the URL which corresponds to a year between 2000-2020
    Returns: either a rendering of error_message.html or subset_display.html depending on validity of user input"""
    filtered_data = database.get_data_from_year(int(year_argument))
    if filtered_data == []:
        return render_template("error_message.html", title="Error!", message="The year that you have entered is invalid.")
    else:
        return render_template("subset_display.html", title="Year subset", field="year", data=year_argument, subset=filtered_data, total_count=database.get_total_for_year(year_argument))


@app.route('/site/<site_argument>', strict_slashes=False)
def get_site_data(site_argument):
    """From the URL input, run the imported production method to fetch the details in the form of a list, then make it presentable. For unavailable URL, return the error message.
    Params: site_argument - a string supplied in the URL which corresponds to a year between 2000-2020
    Returns: either a rendering of error_message.html or subset_display.html depending on validity of user input"""
    filtered_data = (database.get_data_by_site(site_argument))
    if filtered_data == []:
        return render_template("error_message.html", title="Error!", message="The leading site that you have entered is invalid.")
    else:
        return render_template("subset_display.html", title="Site subset", field="leading site", data=site_argument, subset=filtered_data, total_count=database.get_total_for_site(site_argument))


@app.route('/')
def homepage():
    """A simple homepage which lets the user get data by state
    Params: None
    Returns: a rendering of home_page.html"""
    return render_template("home_page.html", title="home page")


@app.route('/about')
def about_us():
    """The About Us page, giving an introduction to the Flask webpages and how to navigate it.
    Params: None
    Returns: a rendering of about_us.html"""
    return render_template("about_us.html", title="About Us")


@app.route('/contact')
def contact_us():
    """The Contact Us page, giving an introduction to the website creators and links to communicate.
    Params: None
    Returns: a rendering of contact_us.html"""
    return render_template("contact_us.html", title="Contact Us")


@app.errorhandler(404)
def page_not_found(e):
    """For when 404 error is encountered, such that a potentially possible but non-existant URL is used such as /year/4444.
    Params: an error value
    Returns: rendering of error_message.html"""
    return render_template("error_message.html", title="Error!", message="The URL that you have entered is invalid.")


@app.errorhandler(500)
def python_bug(e):
    """For when a runtime error is encountered in the code itself.
    Params: an error value
    Returns: rendering of error_message.html"""
    return render_template("error_message.html", title="Error!", message="It seems that a bug has occurred in the codes.")


if __name__ == '__main__':
    load_data()
    app.run(port=5000)  # just using Marshall's port for now
