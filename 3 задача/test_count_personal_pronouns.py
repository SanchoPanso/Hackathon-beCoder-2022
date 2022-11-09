import pytest
from main import count_personal_pronouns

def test_empty():
    string = 'asd qwe rty'
    fp_cnt, other_cnt = count_personal_pronouns(string)

    assert fp_cnt == 0
    assert other_cnt == 0

def test_complex():
    string = 'Я мы. Ты - вы.\n Он,она:оно! текст Они'

    fp_cnt, other_cnt = count_personal_pronouns(string)

    assert fp_cnt == 2
    assert other_cnt == 6
