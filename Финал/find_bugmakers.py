import json


def find_bugs(commit_table: list) -> list:
    """
    :param commit_table: table of commits sorted by time
    :return: list of dict with author and file
    """

    bugs = []

    for idx, commit in enumerate(commit_table):
        if commit['fix'] is True:
            fixed_files = commit['files']

            if idx == len(commits) - 1:
                continue

            for fixed_file in fixed_files:

                for i in range(idx + 1, len(commit_table)):
                    old_commit = commit_table[i]
                    if fixed_file in old_commit["files"]:
                        
                        bugs.append(
                            {
                                "timestamp": old_commit['timestamp'],
                                "author": old_commit['author'],
                                "file": fixed_file,
                            }
                        )

                        break
    
    return bugs

def find_bug_frequency(bugs: list) -> list:
    
    bug_frequencies = {}

    for bug in bugs:
        author = bug['author']
        file = bug['file']

        if author not in bug_frequencies:
            bug_frequencies[author] = {}
        
        if file in bug_frequencies[author]:
            bug_frequencies[author][file] += 1
        else: 
            bug_frequencies[author][file] = 1
    
    return bug_frequencies


def find_commits_numbers(commits: list):
    commits_numbers = {}

    for commit in commits:
        author = commit['author']
        files = commit['files']

        if author not in commits_numbers:
            commits_numbers[author] = {}
        
        for file in files:
            if file in commits_numbers[author]:
                commits_numbers[author][file] += 1
            else: 
                commits_numbers[author][file] = 1

    
    return commits_numbers


def find_statistics(numbers: dict, bug_freq: dict):
    statistic = {}

    for auth_num in numbers:
        author = auth_num['author']

        if author not in statistic:
            statistic[author] = {}
        
        


if __name__ == '__main__':

    with open('./commits.json', 'r') as file:
        commits = json.load(file)
    
    #print(commits)

    bugs = find_bugs(commits)

    freq = find_bug_frequency(bugs)

    numbers = find_commits_numbers(commits)
    print(numbers)



