# Скачать все коммиты в репозитории в файл "commits.txt" в формате: timestamp, id, author, message, files

import shutil
import validators
import os
import sys
import time
import json
from git import Repo


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


def get_url_from_input() -> str:
    """
    Get url from user input and validate it
    :return: url
    """
    while True:
        url = input("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                    "Введите ссылку: ")

        # If url is not valid, then print warning and ask again
        if not validators.url(url):
            print(yellow_text("Некорректная ссылка!"))
            continue

        return url


def get_repo_from_url(url: str) -> Repo:
    """
    Get repository from url
    :param url: url to repository
    :return: repository
    """
    print(green_text("\nСкачивание репозитория... Пожалуйста, подождите, это может занять некоторое время...\n"))
    Repo.clone_from(url, "./repo")


def get_commits_from_repo(repo: Repo):
    """
    Get all commits from repository
    :param repo: repository
    """
    commits = list(repo.iter_commits())

    with open("commits.json", "w", encoding="UTF-8") as file:
        file.write(json.dumps([{"timestamp": commit.committed_datetime.timestamp(), "id": commit.hexsha,
                                "author": commit.author.name, "fix": "fix" in commit.message.lower(),
                                "files": commit.stats.files} for commit in commits],
                              indent=4))

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


# def find_fix_lines():
#     with open("commits.txt", "r", encoding="UTF-8") as file:
#         fix_lines = []
#         for count, line in enumerate(file):
#             if "True" in line:
#                 fix_lines.append(count)
#     return fix_lines
#
#
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

def main():
    if os.path.exists("./repo"):
        os.system("del /f /s /q repo")
        shutil.rmtree("./repo")
    if os.path.exists("./commits.txt"):
        os.remove("./commits.txt")

    url = get_url_from_input()
    get_repo_from_url(url)

    repo = Repo("./repo")
    get_commits_from_repo(repo)

    # fix_lines = find_fix_lines()
    # find_who_made_mistake()


if __name__ == '__main__':
    main()
