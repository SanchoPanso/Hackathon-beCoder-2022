import json
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def find_bugs(commit_table: list) -> list:
    """
    :param commit_table: table of commits sorted by time
    :return: list of dict with author and file
    """

    bugs = []

    for idx, commit in enumerate(commit_table):
        if commit['fix'] is True:
            fixed_files = commit['files']

            if idx == len(commit_table) - 1:
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


def find_statistics1(numbers: dict, bug_freq: dict):
    statistic = {}

    for author in numbers:
        
        if author not in statistic:
            statistic[author] = {}
        
        for file in numbers[author]:
            numbers_of_commits = numbers[author][file]

            if author in bug_freq and file in bug_freq[author]: 
                numbers_of_bugs = bug_freq[author][file]
            else:
                numbers_of_bugs = 0
        
            statistic[author][file] = numbers_of_bugs / numbers_of_commits
    
    return statistic


def find_statistics2(numbers: dict, bug_freq: dict):
    statistic = {}

    for author in numbers:
        
        if author not in statistic:
            statistic[author] = {'x': [], 'y': []}
        
        for file in numbers[author]:
            numbers_of_commits = numbers[author][file]

            if author in bug_freq and file in bug_freq[author]: 
                numbers_of_bugs = bug_freq[author][file]
            else:
                numbers_of_bugs = 0
        
            statistic[author]['y'].append(numbers_of_commits)
            statistic[author]['x'].append(numbers_of_bugs / numbers_of_commits)
    
    return statistic


def prepare_troublefiles_data(numbers: dict, bug_freq: dict, bugs: list, commits: list):
    x, y = [], []
    statistic = find_statistics1(numbers, bug_freq)
    bug_timestamps = [bug['timestamp'] for bug in bugs]

    for commit in commits:
        timestamp = commit['timestamp']
        author = commit['author']
        files = commit['files']

        bug_probs = 0
        for file in files:

            if file in statistic[author]:
                bug_probs += statistic[author][file]
        
        x.append([bug_probs])
        y.append([1] if timestamp in bug_timestamps else [0])

        
        
    return x, y


def otsu(x, y):
    total = sum(y)
    sum_y = sum([i * j for i, j in zip(x, y)])
    sum_y2 = sum([i * i * j for i, j in zip(x, y)])
    max_x = max(x)
    min_x = min(x)
    mean = sum_y / total
    variance = sum_y2 / total - mean * mean
    threshold = (mean - min_x) / (max_x - min_x)
    threshold = threshold * (max_x - min_x) + min_x
    return threshold


def get_hist(x, num=10):
    hist = [0 for i in range(num)]
    for xi in x:
        for i in range(num):
            if i * 1/num <= xi <= (i + 1) * 1/num:
                hist[i] += 1

    return hist 


if __name__ == '__main__':

    with open('./commits.json', 'r') as file:
        commits = json.load(file)
    
    #print(commits)

    bugs = find_bugs(commits)
    freq = find_bug_frequency(bugs)

    numbers = find_commits_numbers(commits)

    statistic = find_statistics1(numbers, freq)
    #author = list(statistic.keys())[0]

    common_error_arr = []
    for author in statistic.keys():
        print(author)
        #print(statistic[author])

        error_arr = [statistic[author][file] for file in statistic[author]]# if statistic[author][file] != 0]
        #print(error_arr)
        common_error_arr += error_arr

    
    pd.Series(common_error_arr).plot(kind='hist', title = 'height', bins=5)
    plt.xlim([0, 1.2])
    

    x = [0.1 * i for i in range(10)]
    y = get_hist(error_arr)
    print(otsu(x, y))
    # plt.axvline(x = otsu(x, y), color = 'b', label = 'axvline - full height')

    plt.show()



    common_x2, common_y2 = [], []
    statistic2 = find_statistics2(numbers, freq)
    reg = LinearRegression()
    for author in statistic2.keys():
        x2 = statistic2[author]['x']
        y2 = statistic2[author]['y']


        x2_tmp, y2_tmp = [], []
        for i in range(len(x2)):
            if x2[i] != 0:
                x2_tmp.append(x2[i])
                y2_tmp.append(y2[i])
        x2, y2 = x2_tmp, y2_tmp
        if len(x2) == 0: x2 = [0]
        if len(y2) == 0: y2 = [0]

        common_x2 += x2
        common_y2 += y2



    reg.fit(np.array([common_x2]).T, np.array([common_y2]).T)

    plt.scatter(common_x2, common_y2)

    line_x = np.arange(0, 1, 0.1)
    line_y = reg.predict(line_x.reshape(-1, 1))
    print(line_x)
    print(line_y)
    plt.plot(line_x, line_y, color='orange')

    plt.xlim([0, 1.2])
    plt.show()


    x, y = prepare_troublefiles_data(numbers, freq, bugs, commits)
    print(len(x))

    x0, y0, x1, y1 = [], [], [], []
    for i in range(len(x)):
        if y[i][0] == 0:
            x0.append(x[i])
            y0.append(y[i])
        else:
            x1.append(x[i])
            y1.append(y[i])
    print('x0', len(x0))
    print('x1', len(x1))
    x1 = x1 * (len(x0) // len(x1))
    y1 = y1 * (len(y0) // len(y1))

    x = x0 + x1
    y = y0 + y1

    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size = 0.3, random_state = 97)


    # train_x, train_y = x[:int(0.8*len(x))], y[:int(0.8*len(y))]
    # test_x, test_y = x[int(0.8*len(x)):], y[int(0.8*len(y)):]
    model = LogisticRegression()
    model.fit(train_x, train_y)
    print(model.score(test_x, test_y))
    test_pred_y = model.predict(test_x)
    print(test_pred_y)
    print('accuracy:', accuracy_score(test_y, test_pred_y))
    print('precision:', precision_score(test_y, test_pred_y))
    print('recall:', recall_score(test_y, test_pred_y))














