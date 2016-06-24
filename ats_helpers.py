"""This module contains helper functions for ATS test module."""

import json


def read_file(path_to_file):
    """Read file and return list."""
    with open(path_to_file) as data_file:
        input_list = data_file.read().splitlines()
    # print data
    return input_list


def append_protocol(url_to_test):
    """Add protocol name to create a valid url."""
    url_to_test = url_to_test.replace("https://", "http://")
    if url_to_test.startswith('http://'):
        # Url starts with protocol: No need to append protocol
        pass
    else:
        url_to_test = "http://" + str(url_to_test)
    return url_to_test


def write_output_to_file(file_name, results_dict):
    """Write input list to a file."""
    with open(file_name, "w") as f:
        json.dump(results_dict, f)
    print("Results stored in ", file_name)


def print_not_passed(results_dict):
    """Print all the domains that didn't pass ATS test."""
    count_not_passed = 0
    print('Number of domains tested:', len(results_dict))
    print("-----Domains failing ATS test-----")
    for k, v in results_dict.items():
        if 'Passed' not in v:
            count_not_passed += 1
            print(k, ' - ', v)
    print("Number of domains that didn't pass ATS test:", count_not_passed)
