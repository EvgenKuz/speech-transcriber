# Генератор транскрипта аудио

>[!IMPORTANT] 
>Использует [AssemblyAI](https://www.assemblyai.com/products/?speech-to-text), поэтому требуется их бесплатный API ключ.

## Установка и запуск

1. Установить [Python 3.11+](https://www.python.org/downloads/)
2. Установить [Poetry](https://python-poetry.org/docs/)
3. Установить зависимости, запустив `poetry install`
4. Создать _.env_ файл:
```dotenv
ASSEMBLYAI_API_KEY=<AssemblyAI API ключ>
```
5. Запустить с помощью `poetry run main.py`

## Разработка

1. Установить [Python 3.11+](https://www.python.org/downloads/)
2. Установить [Poetry](https://python-poetry.org/docs/)
3. Установить зависимости, запустив `poetry install --with dev`
4. Запустить `poetry run pre-commit install`
5. Создать _.env_ файл:
```dotenv
ASSEMBLYAI_API_KEY=<AssemblyAI API ключ>
```
