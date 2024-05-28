import tomllib
from functools import lru_cache
from pathlib import Path

import tomli_w

settings_file = Path("settings.toml")


def create_toml_settings():
    assemblyai_api_key = input("Введите ваш Assembly API ключ: ")

    settings_dict = dict(api=dict(tokens=dict(assemblyai=assemblyai_api_key)))
    with open(settings_file, "w") as file:
        file.write(tomli_w.dumps(settings_dict))

    print(f"\n Файл с настройками ({settings_file}) создан.")


@lru_cache
def load_toml_settings() -> dict:
    with open(settings_file, "r") as file:
        settings_dict = tomllib.loads(file.read())

    return settings_dict
