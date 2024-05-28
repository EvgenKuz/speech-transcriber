from pathlib import Path

import settings
from transcribe_audio import save_transcribed_to_file, transcribe_audio


def main():
    if not settings.settings_file.exists():
        print("Это ваш первый запуск программы, необходимо создать файл с настройками.")
        settings.create_toml_settings()

    settings.load_toml_settings()
    print(f"Настройки загруженый из файла {settings.settings_file}.")

    while True:
        file_location = input("What file to transcribe?\n")
        file = Path(file_location)

        if not file.exists():
            print(f"File ({file_location}) does not exist")
            continue

        break

    transcribed_audio = transcribe_audio(file)
    save_to = f"output/transcribed_{file.name}.txt"
    save_transcribed_to_file(transcribed_audio, save_to, True)

    print(f"File saved to {save_to}")


if __name__ == "__main__":
    main()
