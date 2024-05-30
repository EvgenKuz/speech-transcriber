import traceback
from datetime import datetime
from pathlib import Path

import crossfiledialog
import filetype

import settings
from errors import AudioBiggerThanTwoPointTwoGigabytes, TranscribingError
from transcribe_audio import save_transcribed_to_file, transcribe_audio


def filter_incorrect_file(path: Path) -> bool:
    if path.is_file():
        kind = filetype.guess(str(path))

        if kind is not None and kind.mime.startswith("audio/"):
            return True
        return False
    return False


def load_setting():
    if not settings.settings_file.exists():
        print("Это ваш первый запуск программы, необходимо создать файл с настройками.")
        settings.create_toml_settings()

    settings.load_toml_settings()
    print(f"Настройки загруженый из файла {settings.settings_file}.")


def ask_for_files() -> list[Path]:
    print(
        "Надо ввести путь к аудиофайлу или папке с аудиофайлами, "
        "которые вы хотите транскрибировать."
    )
    files = crossfiledialog.open_multiple("Выберите файл(ы) для транскрибирования")
    path_files = []

    for file in files:
        path = Path(file)
        path_files.append(path)

        if not path.exists():
            print(f"Файл или папка ({path}) не существует. Как?")
            exit(1)

    return path_files


def ask_are_files_correct(files: list[Path]) -> list[Path]:
    files = list(filter(filter_incorrect_file, files))
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

    files = ask_are_files_correct(ask_for_files())

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

        save_to = Path(
            "output",
            f"{file.name}_transcribed_"
            f"{datetime.now().strftime('%d.%m.%YT%H-%M-%S')}.txt",
        )
        save_to.parent.mkdir(exist_ok=True)
        save_transcribed_to_file(transcribed_audio, save_to, False)

        print(f"Файл сохранён как '{save_to}'.")


if __name__ == "__main__":
    main()
