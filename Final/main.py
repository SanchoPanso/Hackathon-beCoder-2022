# Скачать все коммиты в репозитории в файл "commits.txt" в формате: timestamp, id, author, message, files

import shutil
import validators
import os
import sys
import time
# import json
from git import Repo
import bug_parsing

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json


def green_text(text: str) -> str:
    """
    Return green text for console (using ANSI escape sequences)
    :param text: text to color
    :return: green text for console
    """
    return '\033[32m' + text + '\033[0m'


def yellow_text(text: str) -> str:
    """
    Return yellow text for console (using ANSI escape sequences)
    :param text: text to color
    :return: yellow text for console
    """
    return '\033[33m' + text + '\033[0m'


def red_text(text: str) -> str:
    """
    Return red text for console (using ANSI escape sequences)
    :param text: text to color
    :return: red text for console
    """
    return '\033[31m' + text + '\033[0m'

def get_url_from_input() -> str:
    """
    Get url from user input and validate it
    :return: url
    """
    while True:
        url = input("Введите ссылку: ")

        # If url is not valid, then print warning and ask again
        if not validators.url(url):
            print(yellow_text("Некорректная ссылка!"))
            continue

        return url


def get_repo_from_url(url: str):
    """
    Get repository from url
    :param url: url to repository
    """
    print(green_text("\nСкачивание репозитория... Пожалуйста, подождите, это может занять некоторое время...\n"))
    Repo.clone_from(url, "./repo")


def get_commits_from_repo(repo: Repo):
    """
    Get all commits from repository
    :param repo: repository
    """
    commits = list(repo.iter_commits())
    print(green_text("\nФормирование списка коммитов... "
                     "\nПожалуйста, подождите, это может занять") + red_text(" продолжительное ") +
          green_text("время, если коммитов больше тысячи...\n"))
    res = []
    for i, commit in enumerate(commits):
        res.append({"timestamp": commit.committed_datetime.timestamp(),
                    "id": commit.hexsha,
                    "author": commit.author.name,
                    "fix": "fix" in commit.message.lower(),
                    "files": list(commit.stats.files.keys())
                    })

    with open("commits.json", "w", encoding="UTF-8") as file:
        json.dump(res, file)

        # file.write(json.dumps([{"timestamp": commit.committed_datetime.timestamp(), 
        #                         "id": commit.hexsha,
        #                         "author": commit.author.name, 
        #                         "fix": "fix" in commit.message.lower(),
        #                         "files": commit.stats.files} for commit in commits],
        #                       ))

        # for commit in commits:
        #     message = commit.message
        #     fix_flax = False
        #     if "fix" in message.lower():
        #         fix_flax = True
        #     files_list = []
        #     for files_name in commit.stats.files:
        #         files_list.append(files_name)
        #     file.write(
        #         f"{commit.committed_date}, {commit.hexsha}, {commit.author}, {fix_flax}, {files_list}\n")


# _______________________________________________________________________________________________________________________
# Old code for getting commits from repository in text format

# def find_who_made_mistake():
#     with open("commits.txt", "r", encoding="UTF-8") as file:
#         fix_line = []
#         for count, line in enumerate(file):
#             if line.split(", ")[3] == "True":
#                 file_list = line.split(", ")[4:]
#                 file_list = file_list.replace("[", "")
#                 file_list = file_list.replace("]", "")
#                 file_list = file_list.replace("'", "")
#                 file_list = file_list.replace("\n", "")
#                 fix_line.append([count, file_list])
#
#         for line in fix_line:
#             line_num = line[0]
#             file_list = line[1].split(", ")
#             print(file_list)
#
#     print(fix_line)
# _______________________________________________________________________________________________________________________

def check_if_repo_exists() -> bool:
    """
    Check if repository exists
    :return: True if exists, False otherwise
    """
    return os.path.exists("./repo")


def delete_repo_and_commits():
    if sys.platform == "win32":
        if os.path.exists("./repo"):
            os.system("del /f /s /q repo >nul 2>&1")
            shutil.rmtree("./repo")
        if os.path.exists("./commits.txt"):
            os.remove("./commits.txt")
    else:
        if os.path.exists("./repo"):
            os.system("rm -rf repo")
        if os.path.exists("./commits.txt"):
            os.remove("./commits.txt")

def menu():
    """
    Main menu
    """
    if check_if_repo_exists():
        common_error_arr, error_arr, numbers, freq, bugs, commits = bug_parsing.find_errors_if_file()
        print(green_text("\nРепозиторий уже скачан! Повторное скачивание не требуется."))
    else:
        common_error_arr, error_arr, numbers, freq, bugs, commits = [], [], [], [], [], []

    while True:
        print("\n")
        print(green_text("1") + ". Скачать репозиторий и получить все коммиты в файл")
        print(green_text("2") + ". Построить гистограмму для первой гипотезы")
        print(green_text("3") + ". Построить гистограмму для второй гипотезы")
        print(green_text("4") + ". Вывести вероятность ошибки в файле")
        print(green_text("5") + ". Скачать тестовый репозиторий (usememos/memos)")
        print(green_text("0") + ". Удалить все файлы репозитория и информацию о коммитах")
        print(green_text("q") + ". Выход")
        print("Репозиторий для тестов: https://github.com/usememos/memos")

        choice = input("Введите номер пункта меню: ")
        print('\n\n\n\n\n')
        if choice == "1":
            url = get_url_from_input()
            delete_repo_and_commits()
            get_repo_from_url(url)
            get_commits_from_repo(Repo("./repo"))
            common_error_arr, error_arr, numbers, freq, bugs, commits = bug_parsing.find_errors_if_file()
            print(green_text("Репозиторий скачан и все коммиты получены успешно!"))
            continue

        elif choice == "2":
            if not check_if_repo_exists():
                print(red_text("Репозиторий не найден!"))
                continue
            print(green_text("Построение гистограммы для первой гипотезы..."))
            bug_parsing.display_histogram_first(common_error_arr, error_arr)
            continue

        elif choice == "3":
            if not check_if_repo_exists():
                print(red_text("Репозиторий не найден!"))
                continue
            print(green_text("Построение гистограммы для второй гипотезы..."))
            bug_parsing.display_histogram_second(numbers, freq)
            continue

        elif choice == "4":
            if not check_if_repo_exists():
                print(red_text("Репозиторий не найден!"))
                continue
            print(green_text("Вывод вероятности ошибки в файле..."))
            bug_parsing.bug_prediction(numbers, freq, bugs, commits)
            continue

        elif choice == "5":
            delete_repo_and_commits()
            get_repo_from_url("https://github.com/usememos/memos")
            get_commits_from_repo(Repo("./repo"))
            common_error_arr, error_arr, numbers, freq, bugs, commits = bug_parsing.find_errors_if_file()
            print(green_text("Репозиторий скачан и все коммиты получены успешно!"))
            continue

        elif choice == "0":
            print("Удаление всех файлов...")
            delete_repo_and_commits()
            print(green_text("Удаление завершено!"))
            continue

        elif choice == "q":
            print(green_text("Выход..."))
            break

        else:
            print(yellow_text("Некорректный ввод!"))
            continue


def main():
    menu()


if __name__ == '__main__':
    main()
