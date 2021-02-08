# Модуль содержащий вспомогательные функции,
# которые используются остальными модулями


def update_file(path_to_new_file: str, path_to_update_file: str) :
    with open(path_to_new_file, "r") as new_file:
        new_file = '\n' + new_file.read()
        with open(path_to_update_file, "a") as update_file:
            update_file.write(new_file)
