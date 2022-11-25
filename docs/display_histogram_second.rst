2.3. display_histogram_second()
===========
This function outputs a histogram for commits.json, confirming or refuting the second hypothesis:

*The developer is more likely to make errors in files he is working with for the first time.

Accordingly, the more often the user works with a file, the lower the chance of making a mistake in it
The approximated straight line on the graph of the number of times the user works with files should decrease


Usage
~~~~~

.. code-block:: python

    bug_parsing.display_histogram_second(numbers, freq)

Parameters:
    * **numbers**: dict, keys - authors, values - dicts of files and its number of commits for specific author
    * **freq**: dict, dict, keys - authors, values - dicts of files and its number of bugs for specific author

Returns:
    This function has no return value

