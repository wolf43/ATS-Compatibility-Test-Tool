"""This module provides nscurl related functions for ATS test module."""

import os
import platform
import subprocess

FNULL = open(os.devnull, 'w')


def is_nscurl_available():
    """"Check if nscurl is available on running platform."""
    # Check if we are running
    if platform.system() == "Darwin":
        # Get OS x version
        os_x_ver = platform.mac_ver()[0]
        # Convert version to float so that we can compare it
        os_x_ver = float('.'.join(os_x_ver.split('.')[:2]))
        # Check if El Capitan or better
        if os_x_ver >= 10.11:
            return True
    return False


def ats_test_nscurl(url_to_test):
    """Check if a url is compatible with Apple ATS requirements."""
    try:
        result = subprocess.check_output(['/usr/bin/nscurl', '--ats-diagnostics', url_to_test], stderr=FNULL)
        if b"ATS Default Connection\nResult : PASS" in result:
            return "Passed: Compatible with ATS"
        else:
            return "Failed: Not compatible with ATS"
    except subprocess.CalledProcessError as e:
        return "".join(("Error: Error occured, nscurl return code: ", str(e.returncode)))
