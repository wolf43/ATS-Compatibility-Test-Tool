"""This module checks if a url is compatible with Apple ATS."""

# Dependencies
# nscurl - only available since OS X 10.11 El Capitan, will use SSL labs API if not available. Test will be much slower as a result
# Python3
# Python requests - if not running on El Capitan, this will be needed for using SSL labs API
import argparse
from datetime import datetime
from nscurl_python_wrapper import ats_test_nscurl, is_nscurl_available
from ats_helpers import read_file, append_protocol, write_output_to_file, print_not_passed
from ssl_labs import test_ats_ssl_labs


def get_cl_arguments():
    """Get the command line arguments passed by user."""
    parser = argparse.ArgumentParser(prog='ATS tester', description='Test ATS compatibility using nscurl or SSL labs')
    parser.add_argument('-i', '--input_file', nargs='?', help='Input file')
    parser.add_argument('-u', '--input_url', nargs='?', help='Input url')
    args = parser.parse_args()
    return vars(args)['input_file'], vars(args)['input_url']


def run_tests_on_file(file_name):
    """Run the test on a file."""
    results_dict = {}
    input_list = read_file(file_name)
    for i in input_list:
        url_to_test = append_protocol(i)
        if is_nscurl_available():
            result = ats_test_nscurl(url_to_test)
            # print(i, ' - ', result)
        else:
            # Add SSL labs test here if nscurl is not available
            result = test_ats_ssl_labs(url_to_test)
        results_dict[i] = result
    # Write the dictonary to file
    output_filename = "".join((file_name[:-4], '_', str(datetime.now().date()), '_ats_results.json'))
    write_output_to_file(output_filename, results_dict)
    print_not_passed(results_dict)


def main():
    """The main function."""
    input_file, input_url = get_cl_arguments()
    if input_url:
        url_to_test = append_protocol(input_url)
        if is_nscurl_available:
            result = ats_test_nscurl(url_to_test)
        else:
            result = test_ats_ssl_labs(url_to_test)
        print(input_url, ' - ', result)
    if input_file:
        run_tests_on_file(input_file)


if __name__ == '__main__':
    main()
