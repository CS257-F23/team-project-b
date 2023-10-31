from ProductionCode.case_obj import *

class CancerDataset:
    """A class that contains each case (line) from the full data set. """

    def __init__(self, dataset_name):
        self.file = dataset_name  # the .csv dataset file being accessed for the data
        self.list_of_cases = []  # list of cases, each of which is stored as a Case instance
        self.fill_list_of_cases()  # fills the list with cases

    def convert_dataset_into_titles_and_list_of_cases(self):
        """opens the data file, and reads through each line of the file, outputting each to a list"""
        with open(self.file, 'r') as f:  # opens csv file and reads it as a file
            all_lines = f.readlines()  # get all the lines form the file
            # removes first row of csv and returns it in the list titles
            return all_lines[0], all_lines[1:]

    def fill_list_of_cases(self):
        """adds individual Case instances to the list"""
        titles, raw_data = self.convert_dataset_into_titles_and_list_of_cases()
        for i in range(len(raw_data)):  # POSSIBLY CHANGE TO
            # for case in raw_data
            line_entry = split_data_string_to_list(raw_data[i])
            case_entry = Case(
                line_entry[1], line_entry[4], line_entry[5], line_entry[7], line_entry[9])
            self.list_of_cases.append(case_entry)

    # Note: Merge the below get_data_* methods into a single function to obey the Single Purpose Principle

    def get_data_from_year(self, year):
        """Given a valid input year, returns a list of all cases associated with that year"""
        data_for_year = []
        for case in self.list_of_cases:
            if int(case.get_year()) == year:
                data_for_year.append(case.get_details())
        return data_for_year

    def get_data_by_site(self, leading_site):
        """Given a valid input cancer site, returns a list of all cases associated with that site"""
        data_for_site = []
        for case in self.list_of_cases:
            if case.get_leading_site() == leading_site:
                data_for_site.append(case.get_details())
        return data_for_site

    def get_total_for_site(self, leading_site):
        """calculates and returns the total number of cancer incidences for a given site between the years 2000-2020"""
        total_cases = 0
        for case in self.list_of_cases:
            if case.get_leading_site() == leading_site:
                total_cases += int(case.get_count())
        return total_cases

    def get_total_for_year(self, year):
        """calculates and returns the total number of cancer incidences for a given year"""
        total_cases = 0
        for case in self.list_of_cases:
            if case.get_year() == str(year):
                total_cases += int(case.get_count())
        return total_cases

    def get_total_for_year_and_site(self, year, leading_site):
        """Calculates and returns the total number of cancer incidences for the leading cancer site and year specified by the user"""
        total_cases = 0
        for case in self.list_of_cases:
            if (int(case.get_year()) == int(year)) and (case.get_leading_site() == leading_site):
                total_cases += int(case.get_count())
        return total_cases

    def get_top_ten_from_year_and_leading_site(self, year, leading_site):
        """Creates and returns a top ten list of cancer incidences for both Male and Female's based on the user's parameters of year and site"""
        top_ten_unsorted_male = []
        top_ten_unsorted_female = []
        for case in self.list_of_cases:
            if (int(case.get_year()) == int(year)) and (case.get_leading_site() == leading_site):
                if case.get_sex() == "Male":
                    top_ten_unsorted_male.append((
                        int(case.get_count()), case.get_state()))
                else:
                    top_ten_unsorted_female.append((
                        int(case.get_count()), case.get_state()))
        top_ten_sorted_male = sorted(top_ten_unsorted_male, reverse=True)
        top_ten_sorted_female = sorted(top_ten_unsorted_female, reverse=True)
        return {"Male top ten list" : top_ten_sorted_male[:10],  "Female top ten list" : top_ten_sorted_female[:10]}

    def get_total_and_details(self, combination_method, target_datas):
        """List all cases which has one of its data pieces (states/year/etc.) matching the provided information. This is based on the fact that there is no overlapping names between the fields, such as there is no State named Liver.
        The input are:
        - A string ('or'/'and') from combination_method
        - target_datas which is a list of individual data pieces for filtering, like ["Texas","Male","Liver"]
        The output will include:
        - The total [count] of all matched Cases
        - Which target_data has found matched Cases
        - Which target_data has NOT found matched Cases
        - Listing out the details of all matched Cases"""
        total_cases = 0
        sucessfully_matched_data = []
        not_matched_data = list(target_datas)
        data_for_site = []

        for current_case in self.list_of_cases:  # for each Case in the CancerDataset
            verification_output = current_case.verify_match_user_input(
                combination_method, target_datas)  # the Case is tested for matching the user input
            # the Case passed the matching process
            if verification_output['result']:
                # Increase the total [count] of all matched Cases
                total_cases += int(current_case.get_count())

                # Move data that has successfully found corresponding Cases out of the not_matched list into the sucessfully_matched list
                for data in verification_output['matched']:
                    try:
                        # get the index of an item that has been used to sucessfully obtain Cases to be displayed. Raise ValueError if nothing is fond, in which case ignore it.
                        index_of_matched_data = not_matched_data.index(data)
                        # remove that item from the not_matched list. Raises IndexError if it fails to remove an item, which should be impossible without triggering ValueError, but just in case.
                        matched_data = not_matched_data.pop(
                            index_of_matched_data)
                        # Add the matched data to the sucessfully_matched list
                        sucessfully_matched_data.append(matched_data)
                    except ValueError or IndexError:
                        pass

                # Add the full Case data into data_for_site to be displayed.
                data_for_site.append(current_case.get_details())
                pass

        # Craft the output to be rendered into the Template
        return {
            'total count': total_cases,
            'valid input': sucessfully_matched_data,
            'invalid input': not_matched_data,
            'case details': data_for_site
        }
