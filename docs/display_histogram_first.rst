2.2. display_histogram_first()
==============================
The function outputs a histogram for commits.json, confirming or refuting the first hypothesis:

*The developer is more likely to make bugs in the files he works with more often*

Accordingly, the developer either makes mistakes often in the files to work, or not at all.
The histogram should show two peaks (closer to 0 and 1), then the theory is confirmed

Usage
~~~~~

.. code-block:: python

    bug_parsing.display_histogram_first(common_error_arr, error_arr)

Parameters:
    * **common_error_arr** - list of bugabilities
    * **error_arr** - list of bugabilities for specific authors

Returns:
    This function has no return value, only shows a histogram

