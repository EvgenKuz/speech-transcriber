import os
from pathlib import Path

import pytest

from transcribe_audio import save_transcribed_to_file

files_created = []


@pytest.fixture(autouse=True, scope="module")
def set_up_and_tear_down():
    yield
    for file in files_created:
        if file.is_dir():
            os.rmdir(file)
        else:
            os.remove(file)


def test_file_save():
    utterances = [("A", "AAAAA"), ("B", "BBBBB")]

    file_path = Path("test_file.txt")
    files_created.append(file_path)

    save_transcribed_to_file(utterances, file_path)

    assert file_path.exists()

    text_should_be = """Speaker A: AAAAA

Speaker B: BBBBB

"""

    with open(file_path, "r") as created_file:
        text = created_file.read()

    assert text == text_should_be


def test_does_not_overwrite_by_default():
    file_path = Path("test_file_exists.txt")
    files_created.append(file_path)

    with open(file_path, "w") as file:
        file.write("test")

    assert file_path.exists()

    with pytest.raises(FileExistsError):
        save_transcribed_to_file([("", "")], file_path)


def test_does_overwrite():
    file_path = Path("test_file_overwrite.txt")
    files_created.append(file_path)
    original_text = "test"

    with open(file_path, "w") as file:
        file.write(original_text)

    assert file_path.exists()

    save_transcribed_to_file([("A", "a")], file_path, True)

    with open(file_path, "r") as file:
        text = file.read()

    assert original_text != text


def test_does_not_overwrite_folder():
    folder_path = Path("test_folder")
    folder_path.mkdir()
    files_created.append(folder_path)

    assert folder_path.exists()

    with pytest.raises(FileExistsError):
        save_transcribed_to_file([("", "")], folder_path, True)


def test_does_saves_empty_speaker():
    utterances = [(None, "AAAAA"), ("B", "BBBBB")]

    file_path = Path("test_file_None.txt")
    files_created.append(file_path)

    save_transcribed_to_file(utterances, file_path)

    text_should_be = """Speaker None: AAAAA

Speaker B: BBBBB

"""

    with open(file_path, "r") as created_file:
        text = created_file.read()

    assert text == text_should_be
