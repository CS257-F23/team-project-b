
def parse_URL_string_to_list(URL_string_input):
    """Helper function to get_filtered_data. Convert inputs like 'Liver,%202007' from the URL into ['Liver', '2007'] for uses in the method get_total_and_details in watch.py."""
    proper_whitespace_string = URL_string_input.replace("%20", " ")
    separated_target_data = proper_whitespace_string.split(",")
    list_of_target_data = list(separated_target_data)
    striped_list_of_target_data = [data.strip()
                                   for data in list_of_target_data]
    return striped_list_of_target_data

