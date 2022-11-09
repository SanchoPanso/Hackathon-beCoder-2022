import collections
import os
import re
import requests
import validators
from bs4 import BeautifulSoup
from typing import Tuple

# Желтый текст
def yellow_text(text):
    return '\033[33m' + text + '\033[0m'


# Пользователь вводит URL страницы
def get_url_from_input() -> str:

    while True:
        url = input("Введите ссылку: ")

        # If url is not valid, then print warning and ask again
        if not validators.url(url):
            print(yellow_text("Некорректная ссылка!"))
            continue

        return url
    

def download_webpage_text(url: str) -> str:
    response = requests.get(url)
    return response.text


def count_words(word: str, string: str) -> int:
    """Count numbers of specific words in text"""

    pattern = r'\b' + word + r'\b'
    result = re.findall(pattern, string)
    
    return len(result)


def count_personal_pronouns(text: str) -> Tuple[int, int]:
    first_person_pronouns = [
        "я", "мне", "меня", "мной", "мною", 
        "мы", "нас", "нам", "нами",
    ]
    other_person_pronouns = [
        "ты", "тебе", "тебя", "тобой", "тобою",
        "вы", "вас", "вам", "вами",

        "он", "оно", "его", "ему", "им", "нем",
        "она", "её", "ей", "ней",

        "они", "их", "им", "их", "ими", "них",
    ]

    text = text.lower()

    first_person_pronouns_count = 0
    other_person_pronouns_count = 0

    for word in first_person_pronouns:
        first_person_pronouns_count += count_words(word, text)

    for word in other_person_pronouns:
        other_person_pronouns_count += count_words(word, text)

    return first_person_pronouns_count, other_person_pronouns_count


def main():
    url = get_url_from_input()
    page_text = download_webpage_text(url)

    # turn html-text into clean text without tags
    soup = BeautifulSoup(page_text, "html.parser")
    clean_text = soup.text

    first_person_pronouns_count, other_person_pronouns_count = count_personal_pronouns(clean_text)

    # print results
    print("Количество личных местоимений 1-го лица: ", first_person_pronouns_count)
    print("Количество остальных личных местоимений: ", other_person_pronouns_count)

    if first_person_pronouns_count > other_person_pronouns_count:
        print("На странице больше личных местоимений 1-го лица")

    elif first_person_pronouns_count < other_person_pronouns_count:
        print("На странице больше остальных (не 1-го лица) личных местоимений")

    else:
        print("Количество личных местоимений 1-го лица и остальных личных местоимений равны")


if __name__ == "__main__":
    main()
