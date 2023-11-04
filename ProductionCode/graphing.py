import matplotlib.pyplot as plt
#Matplotlib and  numpy
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.use('Agg')

def case_details_as_3d_list(case_details):
    """Helper function to make_dictionary_of_comparison_data(). 
    Transform 1D list of formatted strings like "State: Texas; Year: 2023; Leading Site: Liver; Sex: Male; Count: 31518" 
    to 3D list with each entry being similar to: [["State", "Texas"], ["Year", "2023"], ["Leading Site", "Liver"], ["Sex", "Male"], ["Count", "31518"]]."""
    categorized_details = [case.split(
        "; ") for case in case_details]  # Each case split to ["State: Texas", "Year: 2023", "Leading Site: Liver", "Sex: Male", "Count: 31518"]
    deeply_split_list = []  # Each case split to [["State", "Texas"], ["Year", "2023"], ["Leading Site", "Liver"], ["Sex", "Male"], ["Count", "31518"]]
    for case in categorized_details:  # Actually splititng the cases
        case_as_dictionary = []
        for data in case:  # Considering a unit like "State: Texas"
            key_and_value = data.split(": ")  # Becomes ["State", "Texas"]
            case_as_dictionary.append(key_and_value)
        deeply_split_list.append(case_as_dictionary)
    return deeply_split_list

def sql_output_cases_as_3d_list(sql_output:list):
    """
    Helper function to make_dictionary_of_comparison_data()
    Converts the direct output from sql to a 3d list, allowing for simple integration into existing code.
    The input is a list of tuples, each entry being similar to: ('Alabama', 2003, 'Liver', 'Male', 128)
    Output is a list of 2D list, each entry being similar to: [["State", "Alabama"], ["Year", "2003"], ["Leading Site", "Liver"], ["Sex", "Male"], ["Count", "128"]]
    """
    
    list_3d_output = []
    
    for case in sql_output:
        state_entry = ["State",str(case[0])]
        year_entry = ["Year",str(case[1])]
        leading_site_entry = ["Leading Site",str(case[2])]
        sex_entry = ["Sex",str(case[3])]
        count_entry = ["Count",str(case[4])]
        
        entry_as_list = []
        entry_as_list.append(state_entry)
        entry_as_list.append(year_entry)
        entry_as_list.append(leading_site_entry)
        entry_as_list.append(sex_entry)
        entry_as_list.append(count_entry)
        list_3d_output.append(entry_as_list)
    return list_3d_output

def make_dictionary_of_comparison_data(case_details):
    """Helper function to reformat_to_plot_data(). 
    Input is list of entries like ('Alabama', 2003, 'Liver', 'Male', 128)
    Run sql_output_cases_as_3d_list() to make list of 2D lists like: [["State", "Texas"], ["Year", "2023"], ["Leading Site", "Liver"], ["Sex", "Male"], ["Count", "31518"]]
    Parse through list of 2D entries to gather data to make a dictionary of plotting data, with each dictionary entry being its own dictionary of counts between items of the same category.
    Example output:
    comparison_data = { 
        "State": {"Texas": 42024},
        "Year": {"2023": 42024},
        "Leading Site": {"Liver": 42024},
        "Sex": {"Male": 31518, "Female": 10506}
    """
    #case_details_in_3d = case_details_as_3d_list(case_details)
    case_details_in_3d = sql_output_cases_as_3d_list(case_details)
    comparison_data = {
        "State": {},
        "Year": {},
        "Leading Site": {},
        "Sex": {}
    }

    # Example: [["State", "Texas"], ["Year", "2023"], ["Leading Site", "Liver"], ["Sex", "Male"], ["Count", "31518"]]
    for case in case_details_in_3d:
        data_categories = ["State", "Year", "Leading Site", "Sex"]
        current_count = int(case[4][1])  # 31518

        # Update relevant category's comparison data
        for category_index in range(len(data_categories)):  # Index from 0 to 3
            # For category_index=0, this is "State", for category_index=1, this is "Year", etc.
            category = data_categories[category_index]
            # For category_index=0, this is "Texas", for category_index=1, this is "2023", etc.
            category_data = case[category_index][1]
            # For example, when category_index=0:
            if category_data not in comparison_data[f"{category}"].keys():
                comparison_data[f"{category}"].setdefault(
                    f"{category_data}", current_count)
                # if "Texas" not in comparison_data["State"].keys():
                # Meaning if this is the first time Texas was iterated through
                # Create a dictionary entry in comparison_data["State"] as {"Texas": 31518}
            else:  # Texas has already been iterated through
                comparison_data[f"{category}"][f"{category_data}"] += current_count
                # comparison_data["State"]["Texas"] += current_count

    return comparison_data

def reformat_to_plot_data(case_details):
    """Helper function to display_filtered_and_sorted_data(). 
    Input is list of entries like ('Alabama', 2003, 'Liver', 'Male', 128)
    Parse through the dictionary from make_dictionary_of_comparison_data() and sort them in a way that Matplotlib can use to make bar graphs.
    After running through make_dictionary_of_comparison_data(), the input will become:
    comparison_data = { 
        "State": {"Texas": 42024},
        "Year": {"2023": 42024},
        "Leading Site": {"Liver": 42024},
        "Sex": {"Male": 31518, "Female": 10506}

    And after processiong, output as 
    plotting_data = {
        "State": {"categories": ["Texas"], "counts":[42024]},
        "Year": {"categories": ["2023"], "counts":[42024]},
        "Leading Site": {"categories": ["Liver"], "counts":[42024]},
        "Sex": {"categories": ["Male", "Female"], "counts":[31518, 10506]}
    }
    """
    comparison_data = make_dictionary_of_comparison_data(case_details)

    plotting_data = {  # Reformat gathered data to make the plots
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

def sort_categories_by_counts(categories, counts):
    zip_counts_with_categories = sorted(zip(counts, categories))
    categories = []
    counts = []
    for pair in zip_counts_with_categories:
        categories.append(pair[1])
        counts.append(pair[0])

    return categories, counts


def create_comparison_plot(title, categories, counts, top_bracket):
    """Make a horizontal bar graph displaying the categories (string) in the y-axis and the counts (integers) in the x-axis. The data is sorted by the count of each category. The input is obtained through relevant helper functions that can be found above and passed to this function by the plot_png() functions.
    With a numeric top_bracket as x, return the top x cases with the most counts.
    With top_bracket as 'All', return the full graph.
    """
    categories, counts = sort_categories_by_counts(categories, counts)

    fig, ax = plt.subplots()
    if top_bracket == 'All':  # Display the whole graph
        # Enough space to see everything easily
        fig.set_size_inches(15, len(counts), forward=True)
        bars = ax.barh(categories, counts, height=0.7)
        # Labels to the side, since some bars are so short they clips into the y-axis
        ax.bar_label(bars, label_type='edge')
    else:
        if len(categories) < top_bracket:
            bars = ax.barh(categories, counts)
        else:
            # Only get the top x cases in number
            bars = ax.barh(categories[-top_bracket:], counts[-top_bracket:])
        # fig.set_size_inches(5, 7, forward=True) # Enough space to see everything easily
        # ax.set_xlim(left=100)
        ax.bar_label(bars, label_type='center')

    plt.yticks(wrap=True)
    ax.set_xlabel('Number of cases')
    ax.set_title("Cases by " + title)

    for bar in bars:
        bar.set_color("orange")  # Bars' color

    return fig
