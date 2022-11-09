import collections
import os
import requests
import validators


# Желтый текст
def yellow_text(text):
    return '\033[33m' + text + '\033[0m'


# Скачиваем страницу и сохраняем ее в файл
def webpage(url):
    r = requests.get(url)
    with open("temp_page.html", "w", encoding="utf-8") as file:
        file.write(r.text)
        file.close()


# Пользователь вводит URL страницы и скачиваем ее
def download_webpage():
    c = False
    url = False
    while not c:
        url = input("Введите ссылку: ")
        if validators.url(url):
            c = True
        else:
            print(yellow_text("Некорректная ссылка!"))
    webpage(url)


# Поиск личных местоимений в тексте и подсчет их количества
def count_personal_pronouns():
    first_peron_pronouns = ["я", "мне", "меня", "мной", "мною", "мои", "моё", "моего", "моей", "моем",
                            "моём", "моему", "мою", " моими", "мы", "нас", "нам", "наш", "наша", "наше"]
    other_pronouns = ["ты", "тебе", "тебя", "тобой", "тобою", "твои", "твоё", "твоего", "твоей", "твоем",
                      "твоём", "твоему", "твою", "твоими", "он", "они", "его", "него", "ему",
                      "нему", "ним", "ними", "нём", "нёму", "вы", "вам", "вас", "вами", "ваш", "ваша", "ваше",
                      "вашего", "вашей", "вашем", "вашему", "вашими", "вашу",
                      "вашим", "она", "ее", "её", "неё", "ей", "нее", "ней", "ею", "оно", "них"]

    # Проверка повторяющихся слов в списках
    # print([item for item, count in collections.Counter(first_peron_pronouns).items() if count > 1])
    # print([item for item, count in collections.Counter(other_pronouns).items() if count > 1])

    # Скачиваем страницу
    download_webpage()

    with open("temp_page.html", "r", encoding="utf-8") as file:
        text = file.read()
        file.close()

    # Удаляем все символы кроме букв и пробелов
    text = ''.join([i for i in text if i.isalpha() or i == ' '])

    # Переводим в нижний регистр
    text = text.lower()

    first_person_pronouns_count = 0
    other_pronouns_count = 0

    # Слово не должно являться частью другого слова (например, "я" в слове "яблоко")
    for word in first_peron_pronouns:
        first_person_pronouns_count += text.count(" " + word + " ")
    for word in other_pronouns:
        other_pronouns_count += text.count(" " + word + " ")

    print("Количество личных местоимений 1-го лица: ", first_person_pronouns_count)
    print("Количество остальных личных местоимений: ", other_pronouns_count)

    # Удаляем временный файл
    os.remove("temp_page.html")


def main():
    count_personal_pronouns()


if __name__ == "__main__":
    main()
