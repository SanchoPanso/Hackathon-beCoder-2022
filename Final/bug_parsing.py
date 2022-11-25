import json
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import time
import math

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def find_bugs(commits: list) -> list:
    """
    This functions create list of dict with bugmaker and file
    :param commits: list of commits sorted by time
    :return: list of dict with author and file
    """

    bugs = []

    for idx, commit in enumerate(commits):
        if commit['fix'] is True:
            fixed_files = commit['files']

            if idx == len(commits) - 1:
                continue

            for fixed_file in fixed_files:

                for i in range(idx + 1, len(commits)):
                    old_commit = commits[i]
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


def find_bugability_statistics_1(commits_numbers: dict, bug_freq: list):
    """
    Find 'numbers_of_bugs / numbers_of_commits' for specific file for specific author of a commit

    :param commits_numbers: dict, keys - authors, values - dicts of files and its number of commits for specific author
    :param bug_freq: dict, dict, keys - authors, values - dicts of files and its number of bugs for specific author
    """
    statistic = {}

    for author in commits_numbers:

        if author not in statistic:
            statistic[author] = {}

        for file in commits_numbers[author]:
            numbers_of_commits = commits_numbers[author][file]

            if author in bug_freq and file in bug_freq[author]:
                numbers_of_bugs = bug_freq[author][file]
            else:
                numbers_of_bugs = 0

            statistic[author][file] = numbers_of_bugs / numbers_of_commits

    return statistic


def find_bugability_statistics_2(commit_numbers: dict, bug_freq: list):
    """
    Find for specific author 
    vector x - vector of 'numbers_of_commits' for specific file
    vector y - vector of 'numbers_of_bugs / numbers_of_commits' for specific file

    :param commits_numbers: dict, keys - authors, values - dicts of files and its number of commits for specific author
    :param bug_freq: dict, dict, keys - authors, values - dicts of files and its number of bugs for specific author
    """
    statistic = {}

    for author in commit_numbers:

        if author not in statistic:
            statistic[author] = {'x': [], 'y': []}

        for file in commit_numbers[author]:
            numbers_of_commits = commit_numbers[author][file]

            if author in bug_freq and file in bug_freq[author]:
                numbers_of_bugs = bug_freq[author][file]
            else:
                numbers_of_bugs = 0

            statistic[author]['x'].append(numbers_of_bugs / numbers_of_commits)
            statistic[author]['y'].append(math.log(numbers_of_commits))

    return statistic


def prepare_troublefiles_data(commits_numbers: dict, bug_freq: list, bugs: list, commits: list):
    """
    Find input data for classification of defining trouble files, and namely

    vector x - summary bugability for files
    vector y - 1 if file is troubled and 0 otherwise

    :param commits_numbers: dict, keys - authors, values - dicts of files and its number of commits for specific author
    :param bug_freq: dict, dict, keys - authors, values - dicts of files and its number of bugs for specific author
    :param bugs: list of dict with author, file, timestamp of a specific bug
    :param commits: list of dict of commit info
    """

    x, y = [], []
    statistic_1 = find_bugability_statistics_1(commits_numbers, bug_freq)
    bug_timestamps = [bug['timestamp'] for bug in bugs]

    for commit in commits:
        timestamp = commit['timestamp']
        author = commit['author']
        files = commit['files']

        nonbug_prob = 1
        for file in files:

            if file in statistic_1[author]:
                nonbug_prob *= 1 - statistic_1[author][file]

        x.append([1 - nonbug_prob])
        y.append([1] if timestamp in bug_timestamps else [0])

    return x, y


def prepare_good_reviewer_data(commits_numbers: dict, bug_freq: list, bugs: list, commits: list):
    """
    Find input data for classification of defining trouble files, and namely

    vector x - summary bugability for files
    vector y - 1 if file is troubled and 0 otherwise

    :param commits_numbers: dict, keys - authors, values - dicts of files and its number of commits for specific author
    :param bug_freq: dict, dict, keys - authors, values - dicts of files and its number of bugs for specific author
    :param bugs: list of dict with author, file, timestamp of a specific bug
    :param commits: list of dict of commit info
    """

    x, y = [], []
    statistic_1 = find_bugability_statistics_1(commits_numbers, bug_freq)
    bug_timestamps = [bug['timestamp'] for bug in bugs]

    authors = {}
    cnt = 0
    for i, commit in enumerate(commits):
        author = commit['author']
        if author not in authors:
            authors[author] = cnt
            cnt += 1

    for commit in commits:
        timestamp = commit['timestamp']
        author = commit['author']
        files = commit['files']

        for a in authors:
            nonbug_prob = 1
            for file in files:
                if file in statistic_1[a]:
                    nonbug_prob *= 1 - statistic_1[a][file]

            x.append([1 - nonbug_prob])
            y.append([1] if timestamp in bug_timestamps and a == author else [0])

    return x, y


def find_errors_if_file():
    """
    This function looks for errors in the .json file
    :return: See docs
    """
    with open('./commits.json', 'r') as file:
        commits = json.load(file)

    # print(commits)

    bugs = find_bugs(commits)
    bug_freq = find_bug_frequency(bugs)

    comm_numbers = find_commits_numbers(commits)

    statistic = find_bugability_statistics_1(comm_numbers, bug_freq)
    # author = list(statistic.keys())[0]
    common_error_arr = []
    error_arr = []

    for authors in statistic.keys():
        # print(authors)
        error_arr = [statistic[authors][file] for file in statistic[authors]]  # if statistic[authors][file] != 0]
        common_error_arr += error_arr

    return common_error_arr, error_arr, comm_numbers, bug_freq, bugs, commits


def display_histogram_first(common_error_arr: list, error_arr: list):
    """
    This function displays the histogram of the first hypotesis
    Check the docs for more info
    """
    plt.rcParams.update({'font.size': 14})

    pd.Series(common_error_arr).plot(kind='hist', title='height', bins=5)
    plt.xlim([0, 1.2])

    plt.title('Histogram of errors (Hypothesis 1)')
    plt.xlabel('Error')
    plt.ylabel('Number of files')

    plt.axvline(np.mean(error_arr), color='b', linestyle='solid', linewidth=2)

    plt.show()


def display_histogram_second(numbers: dict, freq: list):
    """
    This function displays the histogram of the second hypotesis
    Check the docs for more info
    """

    plt.rcParams.update({'font.size': 14})

    common_x2, common_y2 = [], []
    statistic2 = find_bugability_statistics_2(numbers, freq)
    reg = LinearRegression()
    for author in statistic2.keys():
        x2 = statistic2[author]['x']
        y2 = statistic2[author]['y']

        x2_tmp, y2_tmp = [], []
        for __i in range(len(x2)):
            if x2[__i] != 0:
                x2_tmp.append(x2[__i])
                y2_tmp.append(y2[__i])
        x2, y2 = x2_tmp, y2_tmp
        if len(x2) == 0:
            x2 = [0]
        if len(y2) == 0:
            y2 = [0]

        common_x2 += x2
        common_y2 += y2

    reg.fit(np.array([common_x2]).T, np.array([common_y2]).T)

    plt.scatter(common_x2, common_y2)

    line_x = np.arange(0, 1, 0.1)
    line_y = reg.predict(line_x.reshape(-1, 1))

    plt.plot(line_x, line_y, color='orange')

    plt.title('Histogram of errors (Hypothesis 2)')
    plt.xlabel('Error')
    plt.ylabel('Number of times working in this file')

    plt.xlim([0, 1.2])
    plt.show()


def predict_bugability(commit: dict, model, commits_numbers: dict, bug_freq: list):
    """
    This function predicts the bugability of a file
    :param commit: dict, commit info
    :param model: model, model for prediction
    :param commits_numbers: dict, keys - authors, values - dicts of files and its number of commits for specific author
    :param bug_freq: dict, dict, keys - authors, values - dicts of files and its number of bugs for specific author
    :return: float, bugability of a file
    """
    timestamp = commit['timestamp']
    author = commit['author']
    files = commit['files']

    statistic_1 = find_bugability_statistics_1(commits_numbers, bug_freq)

    nonbug_prob = 1
    for file in files:

        if file in statistic_1[author]:
            nonbug_prob *= 1 - statistic_1[author][file]

    x = [[1 - nonbug_prob]]
    return model.predict(x)


def bug_prediction(commits_numbers: dict, bug_freq: list, bugs: list, commits: list):
    """
    This function predicts the bugs using logistic regression
    Check the docs for more info
    """
    x, y = prepare_troublefiles_data(commits_numbers, bug_freq, bugs, commits)

    # print(len(x))

    # Simple class balancing ##
    x0, y0, x1, y1 = [], [], [], []

    for i in range(len(x)):
        if y[i][0] == 0:
            x0.append(x[i])
            y0.append(y[i])
        else:
            x1.append(x[i])
            y1.append(y[i])

    x1 = x1 * (len(x0) // len(x1))
    y1 = y1 * (len(y0) // len(y1))

    x = x0 + x1
    y = y0 + y1

    # train-test splitting
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.3, random_state=97)

    # Training
    model = LogisticRegression()
    model.fit(train_x, train_y)

    # Evaluating
    test_pred_y = model.predict(test_x)

    print('\nData for trouble files prediction:')
    print('Accuracy:', accuracy_score(test_y, test_pred_y))
    print('Precision:', precision_score(test_y, test_pred_y))
    print('Recall:', recall_score(test_y, test_pred_y))

    return model


def reviewer_prediction(commits_numbers: dict, bug_freq: list, bugs: list, commits: list):
    """
    This function predicts the bugs using logistic regression
    Check the docs for more info
    """
    x, y = prepare_good_reviewer_data(commits_numbers, bug_freq, bugs, commits)

    # print(len(x))

    # Simple class balancing ##
    x0, y0, x1, y1 = [], [], [], []

    for i in range(len(x)):
        if y[i][0] == 0:
            x0.append(x[i])
            y0.append(y[i])
        else:
            x1.append(x[i])
            y1.append(y[i])

    x1 = x1 * (len(x0) // len(x1))
    y1 = y1 * (len(y0) // len(y1))

    x = x0 + x1
    y = y0 + y1

    # train-test splitting
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.3, random_state=97)

    # Training
    model = LogisticRegression()
    model.fit(train_x, train_y)

    # Evaluating
    test_pred_y = model.predict(test_x)

    print('\nData for trouble files prediction:')
    print('Accuracy:', accuracy_score(test_y, test_pred_y))
    print('Precision:', precision_score(test_y, test_pred_y))
    print('Recall:', recall_score(test_y, test_pred_y))

    return model


def main():
    common_error_arr, error_arr, numbers, freq, bugs, commits = find_errors_if_file()

    display_histogram_first(common_error_arr, error_arr)
    display_histogram_second(numbers, freq)
    bug_prediction(numbers, freq, bugs, commits)


if __name__ == '__main__':
    main()
