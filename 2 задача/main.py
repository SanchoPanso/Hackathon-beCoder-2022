import os


def yellow_text(text: str) -> str:
    """
    Return yellow text for console (using ANSI escape sequences)
    :param text: text to color
    :return: yellow text for console
    """
    return '\033[33m' + text + '\033[0m'


def check_folder() -> str:
    """
    Check if folder exists and return it if it does or ask user to enter folder name again
    :return: folder path + name
    """
    c = False
    folder = False
    while not c:
        folder = input("Введите адрес папки (абсолютный или относительный): ")
        if os.path.isdir(folder):
            c = True
        else:
            print(yellow_text("Некорректный адрес папки!"))
    return folder


def get_files(folder):
    """
    Get list of files in folder
    :param folder: folder to get files from
    :return: list of files in folder
    """
    files = []
    for file in os.listdir(folder):
        files.append(file)
    return files


def find_h2_styles(folder: str, files: list):
    """
    Find h2 styles in files in <style> tags or in .h2 class in .css files, don't read headers.css
    :param folder: folder to find files in
    :param files: list of files to find h2 styles in
    :return: None
    """
    for file in files:
        with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
            text = f.read()
            if file == 'headers.css':
                continue
            elif file.endswith('.css'):
                if '.h2' in text:
                    print(yellow_text(f"Файл {file} содержит стиль для h2:"))
                    style = text[text.find('.h2'):]
                    style = style[:style.find('}') + 1]
                    print(style)
            elif "<style" in text:
                style = text.split("<style")[1].split("</style>")[0]
                if "h2" in style:
                    print(yellow_text(f"Файл {file} содержит стиль для h2:"))
                    style = style[style.find('h2'):]
                    style = style[:style.find('}') + 1]
                    print(style)


def main():
    # Comment this line if you want to enter folder name manually
    folder = check_folder()

    # Uncomment to enter folder name manually
    # folder = "./test"

    files = get_files(folder)
    find_h2_styles(folder, files)


if __name__ == "__main__":
    main()
