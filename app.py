import io

# Flask imports
from flask import Flask, render_template, request, Response
from ProductionCode.datasource import *

# other requirements


def load_data():
    """Create the global 'dataset' variable to used in later functions."""
    global database
    database = DataSource() #from sql

app = Flask(__name__)

@app.route('/stateinfo', methods=['GET', 'POST'])
def state_info_display():
    """a display page for information by state"""
    if request.method == "POST":
        target_state = request.form["state_for_info_page"]
    elif request.method == "GET":
        target_state = request.args["state_for_info_page"]
    total_incidences = database.get_total_for_state(target_state)
    most_common_cancers_list = database.get_ranked_list_for_state(target_state)
    return render_template("state_info_display.html", title = "state info",total_count = total_incidences, state_choice = target_state, list_of_cancers = most_common_cancers_list)

@app.route('/simpsearch', strict_slashes=False, methods=['GET', 'POST'])
def display_number_of_matches(number_of_matches=0):
    """Filter the dataset by 4 input and return the result to be displayed.
    Input includes a State, Year, Site, and Sex, all can either be specified for left as 'Any'
    """
    try: # When accessed using in-page Submit
        # Get user data.
        if request.method == "POST":
            target_state = request.form["state"]
            target_year = request.form["year"]
            target_site = request.form["site"]
            target_sex = request.form["sex"]
        elif request.method == "GET":
            target_state = request.args["state"]
            target_year = request.args["year"]
            target_site = request.args["site"]
            target_sex = request.args["sex"]
    except: # When accessed with nav bar
        target_state = target_year = target_site = target_sex = ""
    all_input_as_one_URL_string = target_state + "," + target_year + "," + target_site + "," + target_sex
    target_list = parse_URL_string_to_list(all_input_as_one_URL_string)
    while "" in target_list:
        target_list.remove("")
    number_of_matches = database.get_simple_search_data(target_list)
    return render_template("simple_search.html",title = "Simple Search", number_of_matches=number_of_matches)

@app.route('/year/<year_argument>', strict_slashes=False)
def get_year_data(year_argument):
    """From the URL input, run the imported production method to fetch the details in the form of a list, then make it presentable. For unavailable URL, return the error message."""
    filtered_data = database.get_data_from_year(int(year_argument))
    if filtered_data == []:
        return render_template("error_message.html", title="Error!", message="The year that you have entered is invalid.")
    else:
        return render_template("subset_display.html", title="Year subset", field="year", data=year_argument, subset=filtered_data, total_count=database.get_total_for_year(year_argument))

@app.route('/site/<site_argument>', strict_slashes=False)
def get_site_data(site_argument):
    """From the URL input, run the imported production method to fetch the details in the form of a list, then make it presentable. For unavailable URL, return the error message."""
    filtered_data = (database.get_data_by_site(site_argument))
    if filtered_data == []:
        return render_template("error_message.html", title="Error!", message="The leading site that you have entered is invalid.")
    else:
        return render_template("subset_display.html", title="Site subset", field="leading site", data=site_argument, subset=filtered_data, total_count=database.get_total_for_site(site_argument))

@app.route('/')
def homepage():
    """A simple homepage which lets the user get data by state"""
    return render_template("home_page.html",title = "home page")

@app.route('/about')
def about_us():
    """The About Us page, giving an introduction to the Flask webpages and how to navigate it."""
    return render_template("about_us.html", title="About Us")


@app.route('/contact')
def contact_us():
    """The Contact Us page, giving an introduction to the website creators and links to communicate."""
    return render_template("contact_us.html", title="Contact Us")


@app.errorhandler(404)
def page_not_found(e):
    """For when 404 error is encountered, such that a potentially possible but non-existant URL is used such as /year/4444."""
    return render_template("error_message.html", title="Error!", message="The URL that you have entered is invalid.")


@app.errorhandler(500)
def python_bug(e):
    """For when a runtime error is encountered in the code itself."""
    return render_template("error_message.html", title="Error!", message="It seems that a bug has occurred in the codes.")


if __name__ == '__main__':
    load_data()
    app.run(port=5117) #just using Marshall's port for now
