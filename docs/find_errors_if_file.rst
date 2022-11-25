2.1. find_errors_if_file()
=========================

The function is required to search for bugmakers in a .json file with commits.

Usage
~~~~~

.. code-block:: python

    common_error_arr, error_arr, numbers, freq, bugs, commits = bug_parsing.find_errors_if_file()

Parameters:
    This function has no parameters

Returns:
    * **common_error_arr** - list of bugabilities
    * **error_arr** - list of bugabilities for specific authors
    * **numbers** - dict, keys - authors, values - dicts of files and its number of commits for specific author
    * **freq** - dict, dict, keys - authors, values - dicts of files and its number of bugs for specific author
    * **bugs** - list of dict with author, file, timestamp of a specific bug


