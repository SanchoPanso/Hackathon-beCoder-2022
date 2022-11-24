1.5. get_commits_from_repo()
===========
This function creates a commits.json file for all commits from the repository. The .json file is created in the same directory as the repository. The .json file contains the following information for each commit:
* commit timestamp
* commit hash
* commit author
* true/false if the commit contains a "fix" in the commit message
* files changed in the commit

Usage
~~~~~

.. code-block:: python

    get_commits_from_repo(Repo('path/to/repo'))

Parameters:
    * repo (Repo): the repository to get commits from

Returns:
    This function has no return value

