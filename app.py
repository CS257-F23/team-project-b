from ProductionCode.watch import *

#Flask imports
from flask import Flask, render_template, request, Response

#Matplotlib and numpy
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#other requirements
import io

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

def case_details_as_3d_list(case_details):
    """Helper function to make_dictionary_of_comparison_data(). 
    Transform 1D list of formatted strings like "State: Texas; Year: 2023; Leading Site: Liver; Sex: Male; Count: 31518" 
    to 3D list with each entry being similar to: [["State", "Texas"], ["Year", "2023"], ["Leading Site", "Liver"], ["Sex", "Male"], ["Count", "31518"]]."""
    categorized_details = [case.split("; ") for case in case_details] # Each case split to ["State: Texas", "Year: 2023", "Leading Site: Liver", "Sex: Male", "Count: 31518"]
    deeply_split_list = [] # Each case split to [["State", "Texas"], ["Year", "2023"], ["Leading Site", "Liver"], ["Sex", "Male"], ["Count", "31518"]]
    for case in categorized_details: # Actually splititng the cases
        case_as_dictionary = []
        for data in case: # Considering a unit like "State: Texas"
            key_and_value = data.split(": ") # Becomes ["State", "Texas"]
            case_as_dictionary.append(key_and_value)
        deeply_split_list.append(case_as_dictionary)
    return deeply_split_list

def make_dictionary_of_comparison_data(case_details):
    """Helper function to reformat_to_plot_data(). 
    Parse through list of entries like [["State", "Texas"], ["Year", "2023"], ["Leading Site", "Liver"], ["Sex", "Male"], ["Count", "31518"]] to gather data to make a dictionary of plotting data, with each dictionary entry being its own dictionary of counts between items of the same category, such as the entry "State" being a dictionary itself with value {"Texas": 42024}."""
    case_details_in_3d = case_details_as_3d_list(case_details)
    
    comparison_data = { 
        "State": {},
        "Year": {},
        "Leading Site": {},
        "Sex": {}
    }
    
    for case in case_details_in_3d: # Example: [["State", "Texas"], ["Year", "2023"], ["Leading Site", "Liver"], ["Sex", "Male"], ["Count", "31518"]]
        
        data_categories = ["State", "Year", "Leading Site", "Sex"]
        current_count = int(case[4][1]) # 31518
        
        # Update relevant category's comparison data
        for category_index in range(len(data_categories)): # Index from 0 to 3
            category = data_categories[category_index] # For category_index=0, this is "State", for category_index=1, this is "Year", etc.
            category_data = case[category_index][1] # For category_index=0, this is "Texas", for category_index=1, this is "2023", etc.
            # For example, in the case that category_index=0:
            if category_data not in comparison_data[f"{category}"].keys(): 
                comparison_data[f"{category}"].setdefault(f"{category_data}", current_count) 
                # if "Texas" not in comparison_data["State"].keys():
                # Meaning if this is the first time Texas was iterated through
                # Create a dictionary entry in comparison_data["State"] as {"Texas": 31518}
            else: # Texas has already been iterated through
                comparison_data[f"{category}"][f"{category_data}"] += current_count
                # comparison_data["State"]["Texas"] += current_count
    
    return comparison_data

def reformat_to_plot_data(case_details):
    """Helper function to create_comparison_plots(). Parse through the dictionary from make_dictionary_of_comparison_data() and sort them in a way that Matplotlib can use to make bar graphs.
    
    For ID3, this input should be:
    comparison_data = { 
        "State": {"Texas": 42024},
        "Year": {"2023": 42024},
        "Leading Site": {"Liver": 42024},
        "Sex": {"Male": 31518, "Female": 10506}
    
    And output as 
    plotting_data = {
        "State": {"categories": ["Texas"], "counts":[42024]},
        "Year": {"categories": ["2023"], "counts":[42024]},
        "Leading Site": {"categories": ["Liver"], "counts":[42024]},
        "Sex": {"categories": ["Male", "Female"], "counts":[31518, 10506]}
    }
    """
    comparison_data = make_dictionary_of_comparison_data(case_details)
    
    plotting_data = { # Reformat gathered data to make the plots
        "State": {
            "categories": list(comparison_data["State"].keys()), 
            "counts": list(comparison_data["State"].values())
            },
        "Year": {
            "categories": list(comparison_data["Year"].keys()), 
            "counts": list(comparison_data["Year"].values())
            },
        "Leading Site": {
            "categories": list(comparison_data["Leading Site"].keys()), 
            "counts": list(comparison_data["Leading Site"].values())
            },
        "Sex": {
            "categories": list(comparison_data["Sex"].keys()), 
            "counts": list(comparison_data["Sex"].values())
            },
    }
    
    return plotting_data

def create_comparison_plot(title, categories, counts):
    """Make a horizontal bar graph displaying the categories (string) in the y-axis and the counts (integers) in the x-axis. The input is obtained through relevant helper functions that can be found above and passed to this function by the plot_png() functions.
    """        

    fig, ax = plt.subplots()

    bars = ax.barh(categories, counts)

    ax.set_xlabel('Number of cases')
    ax.set_title("Cases by " + title)
    ax.bar_label(bars, label_type='center')
    for bar in bars: bar.set_color("orange") # Bars' color
    
    return fig

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

@app.route('/data', strict_slashes=False, methods = ['GET', 'POST'])
def display_hard_coded_data():
    """Run the imported production method to fetch the hard-coded details and present it. Does get the form data initially but overwrite it with the hard-coded data, it's here to prepare for full implementation.
    Only doable thanks to this article: https://towardsdatascience.com/how-to-easily-show-your-matplotlib-plots-and-pandas-dataframes-dynamically-on-your-website-a9613eff7ae3 
    """
    global plotting_data # Made global so that the /plot/*.png routes can work.
    # Get user data. Unused for ID3 but will play a role in the group component
    if request.method == "POST":
        combination_method=request.form["combination"]
        target_data=request.form["filter targets"]
    elif request.method == "GET":
        combination_method=request.args["combination"]
        target_data=request.args["filter targets"]
    target_data = parse_URL_string_to_list(target_data) # The target data needs to be translated into list form for get_total_and_details()
    filtered_data = dataset.get_total_and_details(combination_method, target_data) # Using the target data and combination method, obtain the list of cases matching user input. 
    plotting_data = reformat_to_plot_data(filtered_data['case details'])
    return render_template("information_display.html", title = "Site subset", total_count = filtered_data['total count'], valid_input = filtered_data['valid input'], invalid_input = filtered_data['invalid input'], subset = filtered_data['case details'])

@app.route('/plot/<category>.png')
def plot_png(category):
    """The route that runs create_comparison_plot() and return a .png of the plot. Uses input that is automatically run when the data-displaying webpage is called (For ID3 this is the hard_display.html site)."""
    if category=="Leading%20Site": category == "Leading Site" # The only category with a whitespace
    this_plot_data = plotting_data[f"{category}"]
    fig = create_comparison_plot(f"{category}", this_plot_data["categories"], this_plot_data["counts"])
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/about')
def about_us():
    """The About Us page, giving an introduction to the Flask webpages and how to navigate it."""
    return render_template("about_us.html", title = "About Us")

@app.route('/contact')
def contact_us():
    """The Contact Us page, giving an introduction to the website creators and links to communicate."""
    return render_template("contact_us.html", title = "Contact Us")



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