"""The module contains functions to work with SSL labs API."""

import requests
import json
from time import sleep


def wait_for_seconds(time_in_sec):
    """The function takes in time in seconds and goes to sleep for that time."""
    print("Waiting for " + str(time_in_sec) + " seconds")
    sleep(time_in_sec)
    print("Waited for " + str(time_in_sec) + " seconds")


def result_from_cache(url_to_test):
    """Check if the results are in SSL labs cache."""
    parameters = {'host': url_to_test, 'fromCache': 'on', 'all': 'done'}
    try:
        response_from_ssl_labs = requests.get("https://api.ssllabs.com/api/v2/analyze", params=parameters)
    except Exception as exception:
        print("Error occured when making a request to ", str(url_to_test))
        print("Error: ", str(exception.__doc__))
        print("Details: ", str(exception.message))
    if check_if_response_has_fatal_error(response_from_ssl_labs):
        return "Fatal Error"
    json_parsed_full_response = json.loads(response_from_ssl_labs.text)
    while json_parsed_full_response['status'] != 'READY':
        print("Result not in cache")
        wait_for_seconds(180)
        response_from_ssl_labs = requests.get("https://api.ssllabs.com/api/v2/analyze", params=parameters)
        if check_if_response_has_fatal_error(response_from_ssl_labs):
            return "Fatal Error"
        json_parsed_full_response = json.loads(response_from_ssl_labs.text)
    return json_parsed_full_response


def check_if_response_has_fatal_error(response):
    """https://github.com/ssllabs/ssllabs-scan/blob/stable/ssllabs-api-docs.md has list of errors."""
    json_parsed_full_response = json.loads(response.text)
    if response.status_code == 200 and json_parsed_full_response['status'] != 'ERROR':
        return False
    elif response.status_code == 200 and json_parsed_full_response['status'] == 'ERROR':
        print("Error\nAPI retured 200:Error\nMost likely reason: hostname doesn't seem right")
        return True
    elif response.status_code == 429:
        print("Error\nClient request rate too high")
        wait_for_seconds(60)
        return False
    elif response.status_code == 400:
        print("Error\nInvalid parameters\nCheck parameters and try again")
        return True
    elif response.status_code == 503:
        print("Service is not available")
        return False
    elif response.status_code == 529:
        print("Error\nService is overloaded")
        return False
    else:
        print("Error\nUnexpected response\nStatus: " + str(response.status_code))
        print("Response text:\n" + str(response.text()))
        return True


def ios_ats_test(json_parsed_full_response):
    """Test if compatible with Apple ATS - https://developer.apple.com/library/ios/releasenotes/General/WhatsNewIniOS/Articles/iOS9.html."""
    count_of_endpoints_ats_errors = 0
    try:
        for i in json_parsed_full_response['endpoints']:
            for j in i['details']['sims']['results']:
                if j['client']['name'] == "Apple ATS":
                    if j['errorCode'] != 0:
                        count_of_endpoints_ats_errors += 1
                    # -------------Test case failed-----------------
                else:
                    pass
                    # +++++++++++++Test case passed++++++++++++++++++
        if count_of_endpoints_ats_errors == 0:
            return "Passed: Compatible with ATS"
        else:
            return "".join(("Failed: ", str(count_of_endpoints_ats_errors), " endpoints are not compatible"))
    except KeyError:
        return "Error: Error in ATS response from SSL labs"


def print_json_parsed_response(json_parsed_full_response):
    """The prints the json object retured by ssl labs nicely."""
    print("Status: " + str(json_parsed_full_response['status']))
    print(json.dumps(json_parsed_full_response, indent=4))


def test_ats_ssl_labs(url_to_test):
    """Function that abstracts the details of SSL labs API and returns simple results to ATS."""
    response = result_from_cache(url_to_test)
    if response == "Fatal Error":
        ats_test_result = "Error: Error during testing with SSL labs API"
    else:
        ats_test_result = ios_ats_test(response)
    return ats_test_result
