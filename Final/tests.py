import pytest
import json
import os.path
from bug_parsing import find_bugs
from bug_parsing import find_bug_frequency
from bug_parsing import find_commits_numbers
from bug_parsing import find_bugability_statistics_1
from bug_parsing import find_errors_if_file
from bug_parsing import bug_prediction

def test_commit_1():
    with open("test_source\\test_1.json", 'r') as file:
        commits = json.load(file)
    ground_truth = [{'timestamp': 800, 'author': 'bugmaker', 'file': 'web/src/components/MemoResources.tsx'},
                    {'timestamp': 800, 'author': 'bugmaker', 'file': 'web/src/less/memo-resources.less'}]
    bugs = find_bugs(commits)
    assert bugs == ground_truth

def test_commit_2():
    with open("test_source\\test_2.json", 'r') as file:
        commits = json.load(file)
    ground_truth = []
    bugs = find_bugs(commits)
    assert bugs == ground_truth

def test_commit_3(): 
    with open("test_source\\test_3.json", 'r') as file:
        commits = json.load(file)
    ground_truth = [{'timestamp': 800, 'author': 'bugmaker_1', 'file': 'web/src/components/MemoResources.tsx'},
                    {'timestamp': 500, 'author': 'bugmaker_2', 'file': 'web/src/less/memo-resources.less'}]
    bugs = find_bugs(commits)
    assert bugs == ground_truth

def test_commit_4():
    with open("test_source\\test_4.json", 'r') as file:
        commits = json.load(file)
    bugs = find_bugs(commits)
    new_list = find_bug_frequency(bugs)
    ground_truth = {'bugmaker_1': {'web/src/components/MemoResources.tsx': 1},
                     'bugmaker_2': {'web/src/less/memo-resources.less': 2}}
    assert new_list == ground_truth

def test_commit_5():
    with open("test_source\\test_1.json", 'r') as file:
        commits = json.load(file)
    bugs = find_bugs(commits)
    new_list = find_bug_frequency(bugs)
    gt = {'bugmaker': {'web/src/components/MemoResources.tsx': 1, 'web/src/less/memo-resources.less': 1}}
    assert new_list == gt

def test_commit_6():
    with open("test_source\\test_2.json", 'r') as file:
        commits = json.load(file)
    bugs = find_bugs(commits)
    new_list = find_bug_frequency(bugs)
    gt = {}
    assert new_list == gt

def test_commit_7():
    with open("test_source\\test_3.json", 'r') as file:
        commits = json.load(file)
    bugs = find_bugs(commits)
    new_list = find_bug_frequency(bugs)
    gt = {'bugmaker_1': {'web/src/components/MemoResources.tsx': 1}, 'bugmaker_2': {'web/src/less/memo-resources.less': 1}}
    assert new_list == gt

def test_commit_8():
    with open("test_source\\test_4.json", 'r') as file:
        commits = json.load(file)
    comm_numbers = find_commits_numbers(commits)
    gt = {'fixer': {'web/src/components/MemoResources.tsx': 1, 'web/src/less/memo-resources.less': 2},
                    'clearcodemaker': {'clearcode.cpp': 1, 'clearcode.py': 1},
                    'bugmaker_1': {'clearcode.cpp': 1, 'clearcode.py': 1, 'web/src/components/MemoResources.tsx': 1},
                    'clearcoder': {'clearcode.cpp': 1, 'clearcode.py': 1, 'web/src/components/MemoResources.tsx': 1},
                    'bugmaker_2': {'clearcode.cpp': 2, 'clearcode.py': 2, 'web/src/less/memo-resources.less': 2}}
    assert comm_numbers == gt 

def test_commit_9():
    with open("test_source\\test_3.json", 'r') as file:
        commits = json.load(file)
    comm_numbers = find_commits_numbers(commits)
    gt = {'fixer': {'web/src/components/MemoResources.tsx': 1, 'web/src/less/memo-resources.less': 1},
                    'clearcodemaker': {'clearcode.cpp': 1, 'clearcode.py': 1},
                    'bugmaker_1': {'clearcode.cpp': 1, 'clearcode.py': 1, 'web/src/components/MemoResources.tsx': 1},
                    'clearcoder': {'clearcode.cpp': 1, 'clearcode.py': 1, 'web/src/components/MemoResources.tsx': 1},
                    'bugmaker_2': {'clearcode.cpp': 1, 'clearcode.py': 1, 'web/src/less/memo-resources.less': 1}}
    assert comm_numbers == gt    

def test_commit_10():
    with open("test_source\\test_2.json", 'r') as file:
        commits = json.load(file)
    comm_numbers = find_commits_numbers(commits)
    gt = {'fixer': {'web/src/components/MemoResources.tsx': 1, 'web/src/less/memo-resources.less': 1},
                    'clearcodemaker': {'clearcode.cpp': 1, 'clearcode.py': 1},
                    'bugmaker': {'clearcode.cpp': 1, 'clearcode.py': 1, 'web/src/components/MemoResources.tsx': 1, 'web/src/less/memo-resources.less': 1}}
    assert comm_numbers == gt              

def test_commit_11():
    with open("test_source\\test_1.json", 'r') as file:
        commits = json.load(file)
    comm_numbers = find_commits_numbers(commits)
    gt = {'fixer': {'web/src/components/MemoResources.tsx': 1, 'web/src/less/memo-resources.less': 1},
                    'clearcodemaker': {'clearcode.cpp': 1, 'clearcode.py': 1},
                    'bugmaker': {'clearcode.cpp': 1, 'clearcode.py': 1, 'web/src/components/MemoResources.tsx': 1, 'web/src/less/memo-resources.less': 1}}
    assert comm_numbers == gt 

def test_commit_12():
    with open("test_source\\test_1.json", 'r') as file:
        commits = json.load(file)
    bugs = find_bugs(commits)
    bug_freq = find_bug_frequency(bugs)
    comm_numbers = find_commits_numbers(commits)
    statistic = find_bugability_statistics_1(comm_numbers, bug_freq)
    gt = {'fixer': {'web/src/components/MemoResources.tsx': 0.0, 'web/src/less/memo-resources.less': 0.0}, 'clearcodemaker': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0}, 'bugmaker': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0, 'web/src/components/MemoResources.tsx': 1.0, 'web/src/less/memo-resources.less': 1.0}}
    assert statistic == gt 

def test_commit_13():
    with open("test_source\\test_2.json", 'r') as file:
        commits = json.load(file)
    bugs = find_bugs(commits)
    bug_freq = find_bug_frequency(bugs)
    comm_numbers = find_commits_numbers(commits)
    statistic = find_bugability_statistics_1(comm_numbers, bug_freq)
    gt = {'fixer': {'web/src/components/MemoResources.tsx': 0.0, 'web/src/less/memo-resources.less': 0.0}, 'clearcodemaker': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0}, 'bugmaker': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0, 'web/src/components/MemoResources.tsx': 0.0, 'web/src/less/memo-resources.less': 0.0}}
    assert statistic == gt     

def test_commit_14():
    with open("test_source\\test_3.json", 'r') as file:
        commits = json.load(file)
    bugs = find_bugs(commits)
    bug_freq = find_bug_frequency(bugs)
    comm_numbers = find_commits_numbers(commits)
    statistic = find_bugability_statistics_1(comm_numbers, bug_freq)
    gt = {'fixer': {'web/src/components/MemoResources.tsx': 0.0, 'web/src/less/memo-resources.less': 0.0}, 'clearcodemaker': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0}, 'bugmaker_1': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0, 'web/src/components/MemoResources.tsx': 1.0}, 'clearcoder': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0, 'web/src/components/MemoResources.tsx': 0.0}, 'bugmaker_2': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0, 'web/src/less/memo-resources.less': 1.0}}
    assert statistic == gt  

def test_commit_15():
    with open("test_source\\test_4.json", 'r') as file:
        commits = json.load(file)
    bugs = find_bugs(commits)
    bug_freq = find_bug_frequency(bugs)
    comm_numbers = find_commits_numbers(commits)
    statistic = find_bugability_statistics_1(comm_numbers, bug_freq)
    gt = {'fixer': {'web/src/components/MemoResources.tsx': 0.0, 'web/src/less/memo-resources.less': 0.0}, 'clearcodemaker': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0}, 'bugmaker_1': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0, 'web/src/components/MemoResources.tsx': 1.0}, 'clearcoder': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0, 'web/src/components/MemoResources.tsx': 0.0}, 'bugmaker_2': {'clearcode.cpp': 0.0, 'clearcode.py': 0.0, 'web/src/less/memo-resources.less': 1.0}}
    assert statistic == gt 

if __name__ == '__main__':
    pass