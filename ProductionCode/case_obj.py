class Case:
    """An object that represents an individual line of the data file. Contains the total number of individuals with cancer for
    each unique combination of state,year,cancer-site, and gender."""

    def __init__(self, state, year, leading_site, sex, count):
        self.state = state
        self.year = year
        self.leading_site = leading_site
        self.sex = sex
        self.count = count

    possible_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                       'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    possible_years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
                      2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    possible_years = [str(year) for year in possible_years]

    possible_leading_sites = ['Brain and Other Nervous System', 'Breast', 'Cervix Uteri', 'Colon and Rectum', 'Corpus Uteri', 'Esophagus', 'Gallbladder', 'Kidney and Renal Pelvis', 'Larynx', 'Leukemias', 'Liver',
                              'Lung and Bronchus', 'Melanoma of the Skin', 'Myeloma', 'Non-Hodgkin Lymphoma', 'Oral Cavity and Pharynx', 'Ovary', 'Pancreas', 'Prostate', 'Stomach', 'Thyroid', 'Urinary Bladder invasive and in situ']

    possible_sexes = ['Female', 'Male']

    def get_details(self):
        return (f"State: {self.state}; Year: {self.year}; Leading Site: {self.leading_site}; Sex: {self.sex}; Count: {self.count}")

    def get_state(self):
        return self.state

    def get_year(self):
        return self.year

    def get_leading_site(self):
        return self.leading_site

    def get_sex(self):
        return self.sex

    def get_count(self):
        return self.count

    def verify_match_user_input(self, combination_method, target_datas):
        """Translate the multiple arguments in target_datas entered by users to filter the primary dataset for output in the get_total_and_details() method. 

        The target_datas arguments can be in any order, but must be separated by commas. The arguments can have whitespaces, but they will be split by commas.

        The returned result is the dictionary of the relevant elements of a Case instance, as well as whether to combine them by an OR or AND operator. the combination_method only works with 'or' or 'and'.

        Further explanations in the templates/home_page.html file.

        """
        flags = {
            'state': 'untracked',
            'year': 'untracked',
            'leading_site': 'untracked',
            'sex': 'untracked'
        }
        output = {
            'result': False,
            'matched': []
        }

        for current_target_data in target_datas:
            # If the target data is in one of the possible fields (state, year, etc.), the field itself is considered to be tracked but 'not matched'. This is used only for the 'and' combination_method
            # If self's corresponding field is a target data, the field and the target data is considered to be 'matched'
            if current_target_data in self.possible_states:
                flags['state'] = 'not matched'
                if self.get_state() in target_datas:
                    flags['state'] = 'matched'
                    output['matched'].append(self.get_state())
            elif current_target_data in self.possible_years:
                flags['year'] = 'not matched'
                if self.get_year() in target_datas:
                    flags['year'] = 'matched'
                    output['matched'].append(self.get_year())
            elif current_target_data in self.possible_leading_sites:
                flags['leading_site'] = 'not matched'
                if self.get_leading_site() in target_datas:
                    flags['leading_site'] = 'matched'
                    output['matched'].append(self.get_leading_site())
            elif current_target_data in self.possible_sexes:
                flags['sex'] = 'not matched'
                if self.get_sex() in target_datas:
                    flags['sex'] = 'matched'
                    output['matched'].append(self.get_sex())

        # Checking if the verification 'result' is True
        if combination_method == 'or' and 'matched' in flags.values():
            # if the combination_method is 'or', this Case can be included in the result as long as any of self's field match a targeted data
            output['result'] = True
        elif combination_method == 'and' and 'matched' in flags.values() and 'not matched' not in flags.values():
            # if the combination_method is 'and', this Case can be included in the result only if there is at least 1 'matched' field (meaning user did ask for information in that field and this Case satisfies it) and the rest are 'untracked' fields (meaning user did not ask for information in that field).
            output['result'] = True

        return output


def split_data_string_to_list(string_with_commas):
    """Split a string read from the .csv file into a convenient list, so it can be indexed.
    It also removes new line, if that's at the end of the last item.
    If the list is empty, return empty list"""
    split_entry = string_with_commas.split(",")
    # if split_entry[9][len(split_entry[9])-1] == "\n":
    split_entry[-1] = split_entry[-1].strip("\n")
    return split_entry