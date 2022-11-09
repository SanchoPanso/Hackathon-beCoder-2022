import os


# Желтый текст
def yellow_text(text):
    return '\033[33m' + text + '\033[0m'


# Пользователь вводит адрес папки и проверяется наличие папки
def check_folder():
    c = False
    folder = False
    while not c:
        folder = input("Введите адрес папки (абсолютный или относительный): ")
        if os.path.isdir(folder):
            c = True
        else:
            print(yellow_text("Некорректный адрес папки!"))
    return folder


# Поиск файлов в папке
def get_files(folder):
    files = []
    for file in os.listdir(folder):
        files.append(file)
    return files


# Функция ищет файлы со стилями заголовков H2, исключая headers.css и удаляет стили на H2 из них
# если, конечно, стиль заголовка H2 записан как h2 { ... }
def delete_h2_styles(folder, files):
    for file in files:
        if file != 'headers.css':
            with open(folder + "/" + file, 'r') as f:
                text = f.read()
                f.close()
                if 'h2 {' in text:
                    text = text.replace('h2 {', 'h2 {display: none;')
                    with open(folder + "/" + file, 'w') as f:
                        f.write(text)


def main():
    folder = check_folder()
    files = get_files(folder)
    delete_h2_styles(folder, files)


if __name__ == "__main__":
    main()
