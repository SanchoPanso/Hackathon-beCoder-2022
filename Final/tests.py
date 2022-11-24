import pytest
import json
import os
from find_bugmakers import find_bugs

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

if __name__ == '__main__':
    #test_commit_1()
    #test_commit_2()
    test_commit_3()