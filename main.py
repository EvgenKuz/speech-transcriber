import traceback
from pathlib import Path

import filetype

import settings
from errors import AudioBiggerThanTwoPointTwoGigabytes, TranscribingError
from transcribe_audio import save_transcribed_to_file, transcribe_audio


def get_files_list(path: Path) -> list[Path]:
    if path.is_file():
        kind = filetype.guess(str(path))

        if kind is not None and kind.mime.startswith("audio/"):
            return [path]
        return []

    files = []

    for file in path.iterdir():
        files.extend(get_files_list(file))

    return files


def load_setting():
    if not settings.settings_file.exists():
        print("Это ваш первый запуск программы, необходимо создать файл с настройками.")
        settings.create_toml_settings()

    settings.load_toml_settings()
    print(f"Настройки загруженый из файла {settings.settings_file}.")


def ask_for_files() -> Path:
    while True:
        path = input(
            "Введите путь к аудиофайлу или папке с аудиофайлами, "
            "которые вы хотите транскрибировать (По-умолчанию: input/): "
        )
        if not path:
            path = "input/"
        path = Path(path)

        if not path.exists():
            print(f"Файл или папка ({path}) не существует.")
            continue

        break

    return path


def ask_are_files_correct(path: Path) -> list[Path]:
    files = get_files_list(path)
    if not files:
        print("Не удалась найти ни одного аудиофайла.")
        exit(1)
    print("Найденные аудиофайлы:")
    for file in files:
        print("\t-", file)
    print()

    while True:
        agreed = (
            input(
                "Эти файлы будут отправлены на сервер AssemblyAI"
                " для траскрибирования. Согласны?(д/н): "
            )
            .lower()
            .strip()
        )
        match agreed:
            case "д":
                break
            case "н":
                exit(0)
            case _:
                print("Необходимо набрать 'д' или 'н'.")

    return files


def main():
    load_setting()

    path = ask_for_files()
    files = ask_are_files_correct(path)

    for file in files:
        print(f"\nНачалась обработка файла '{file}'...")

        try:
            transcribed_audio = transcribe_audio(file)
        except AudioBiggerThanTwoPointTwoGigabytes:
            print(
                f"Файл ({file}) не может быть обработан, "
                "так как его размер привышает 2.2 Гб."
            )
            continue
        except TranscribingError:
            print("Во время транскрибирования произошла ошибка. Детали в log.txt")
            with open("log.txt", "a") as log:
                log.write(traceback.format_exc())
                log.write("\n")
            continue

        save_to = f"output/{file.name}_transcribed.txt"
        save_transcribed_to_file(transcribed_audio, save_to, True)

        print(f"Файл сохранён как '{save_to}'.")


if __name__ == "__main__":
    main()
