import io

# Flask imports
from flask import Flask, render_template, request, Response
from ProductionCode.datasource import *
from ProductionCode.graphing import *

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
        target_state = "any_state"
        target_year = "any_year"
        target_site = "any_site"
        target_sex = "any_sex"
    all_input_as_one_URL_string = target_state + "," + target_year + "," + target_site + "," + target_sex
    target_state = parse_URL_string_to_list(all_input_as_one_URL_string)
    #TODO remove sort out, since we're just using a dropdown menu!
    invalid_query_parameters, valid_column_and_query_parameters = sort_out_invalid_and_valid_query_parameters_with_column(target_state)
    sql_for_number_of_matches = construct_multiargument_query_specified_targets("and",["SUM(case_count)"],valid_column_and_query_parameters)
    #TODO make a method in datasource that does the above; weird to call run_sql_command here
    number_of_matches = database.run_sql_command_and_return_result(sql_for_number_of_matches)
    number_of_matches = number_of_matches[0][0] # Extract from [(3,)] to 3
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

#TODO: clean/remove code below: non essential (besides main of course)

@app.route('/<combination_method>/<target_datas>', strict_slashes=False)
def get_filtered_data(combination_method, target_datas):
    """From the URL input, run the imported production method to fetch the details in the form of a dictionary consisting of: 
        - 'total count': The total [count] of all matched Cases
        - 'valid input': Which target_data has found matched Cases
        - 'invalid input': Which target_data has NOT found matched Cases
        - 'case details': Listing out the details of all matched Cases
    For unavailable URL, return the error message."""
    filtered_data = database.get_total_and_details(
        combination_method, parse_URL_string_to_list(target_datas))
    if filtered_data["total count"] == 0:
        return render_template("error_message.html", title="Error!", message="The input that you have entered has no matching cases.")
    else:
        return render_template("information_display.html", title="Site subset", total_count=filtered_data['total count'], valid_input=filtered_data['valid input'], invalid_input=filtered_data['invalid input'], subset=filtered_data['case details'])


@app.route('/data', strict_slashes=False, methods=['GET', 'POST'])
def display_filtered_and_sorted_data():
    """Filter the dataset and return the result to be displayed.
    Input includes:
    - target_data: entries like 'Liver' and '2018' to filter the dataset by
    - combination_method: combine target_data by either 'and' or 'or' combination when filtering
    - top_bracket: in the information display page, preview only the top 3/4/5/6/7 most common cases
    Only doable thanks to this article: https://towardsdatascience.com/how-to-easily-show-your-matplotlib-plots-and-pandas-dataframes-dynamically-on-your-website-a9613eff7ae3 
    """
    # Get user data.
    if request.method == "POST":
        target_data = request.form["filter targets"]
        combination_method = request.form["combination"]
        top_bracket = request.form["top bracket"]
    elif request.method == "GET":
        target_data = request.args["filter targets"]
        combination_method = request.args["combination"]
        top_bracket = request.args["top bracket"]
    # The target data needs to be translated into list form for get_total_and_details()
    target_data = parse_URL_string_to_list(target_data)
    # Using the target data and combination method, obtain the list of cases matching user input.
    #filtered_data = dataset.get_total_and_details(combination_method, target_data)
    # Made global so that the /plot/*.png routes can work.
    global plotting_data
    filter_result = database.return_variable_arguments_query_result(combination_method, target_data)
    total_count = filter_result['total count']
    valid_input=filter_result['valid input']
    invalid_input=filter_result['invalid input']
    subset=filter_result['subset']
    plotting_data = reformat_to_plot_data(subset)
    return render_template("information_display.html", title="Site subset", total_count=total_count, valid_input=valid_input, invalid_input=invalid_input, subset=subset, top_bracket=top_bracket)

@app.route('/plot/<category>/<top_bracket>.png')
def plot_png(category, top_bracket):
    """The route that runs create_comparison_plot() and return a .png of the plot. 
    Uses input that is automatically run when the data-displaying webpage is called (category) and user input (top_bracket).
    """

    if category == "Leading%20Site":
        category == "Leading Site"  # The only category with a whitespace
    try:
        top_bracket = int(top_bracket)  # Convert the top_bracket to int
    except ValueError:
        pass  # Except if top_bracket is 'All'

    this_plot_data = plotting_data[f"{category}"]
    fig = create_comparison_plot(
        f"{category}", this_plot_data["categories"], this_plot_data["counts"], top_bracket)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/yearandsite')
def state_and_site_form():
    return render_template("year_and_site.html",title="year and Site form")

@app.route('/rankedLists', methods = ["GET","POST"])
def display_ranked_List():
    if request.method == "POST":
        target_year = request.form["year_for_ranked"]
        target_site = request.form["site_for_ranked"]
    elif request.method == "GET":
        target_year = request.args["year_for_ranked"]
        target_site = request.args["site_for_ranked"]

    top_10_lists = database.get_ranked_list_by_year_and_site(target_year,target_site)
    female_list = top_10_lists["Female top ten list"]
    male_list = top_10_lists["Male top ten list"]
    return render_template("top_10_page.html",title = "State and Site display",year_choice = target_year, site_choice = target_site, flist = female_list, mlist = male_list)

@app.route('/advsearch')
def advancedSearchPage():
    """Lets the user utilize a complicated advanced search method that ouputs graphs."""
    return render_template("adv_search.html", title="advanced search")

if __name__ == '__main__':
    load_data()
    app.run(port=5117) #just using Marshall's port for now
