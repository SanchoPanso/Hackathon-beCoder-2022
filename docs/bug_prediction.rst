1.4. bug_prediction()
=====================
This function split the data into training and testing data and then train the model on the training data and predict the bug on the testing data. It also calculates the accuracy of the model.

Usage
~~~~~

.. code-block:: python

    bug_parsing.bug_prediction(numbers, freq, bugs, commits)

Parameters:
    * **numbers**: dict, keys - authors, values - dicts of files and its number of commits for specific author
    * **freq**: dict, dict, keys - authors, values - dicts of files and its number of bugs for specific author
    * **bugs**: list of dict with author, file, timestamp of a specific bug
    * **commits**: list of dict of commit information

Returns:
    This function has no return value, only prints the accuracy of the model.

