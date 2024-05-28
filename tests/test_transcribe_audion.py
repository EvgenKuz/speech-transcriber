import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from errors import AudioBiggerThanTwoPointTwoGigabytes, TranscribingError
from transcribe_audio import transcribe_audio

files_created = []


@pytest.fixture(autouse=True, scope="module")
def set_up_and_tear_down():
    yield
    for file in files_created:
        if file.is_dir():
            os.rmdir(file)
        else:
            os.remove(file)


def test_file_does_not_exist():
    file_not_exists = Path("does_not_exist")

    assert not file_not_exists.exists()

    with pytest.raises(FileNotFoundError):
        transcribe_audio(file_not_exists)


def test_file_is_folder():
    folder = Path("folder_test")
    folder.mkdir()
    files_created.append(folder)

    assert folder.exists()

    with pytest.raises(FileNotFoundError):
        transcribe_audio(folder)


@patch("pathlib.Path.stat")
def test_file_size_bigger_than_2_point_two_gigabytes(stat_result):
    file = Path("file_test")
    files_created.append(file)

    with open(file, "w") as f:
        f.write("test")

    stat_result.return_value.st_size = 3 * 1024 * 1024 * 1024
    stat_result.return_value.st_mode = os.stat(str(file)).st_mode

    with pytest.raises(AudioBiggerThanTwoPointTwoGigabytes):
        transcribe_audio(file)

    assert stat_result.called


@patch("assemblyai.Transcriber.transcribe")
def test_trinscriber_errors(transcribe):
    file = Path("file_test_errors")
    files_created.append(file)

    with open(file, "w") as f:
        f.write("test")

    transcribe.return_value.error = "error"

    with pytest.raises(TranscribingError):
        transcribe_audio(file)


@patch("assemblyai.Transcriber.transcribe")
def test_trinscribed_to_none(transcribe):
    file = Path("file_test_None")
    files_created.append(file)

    with open(file, "w") as f:
        f.write("test")

    transcribe.return_value.error = []
    transcribe.return_value.utterances = None

    transcript = transcribe_audio(file)

    assert isinstance(transcript, list)
    assert len(transcript) == 0


@patch("assemblyai.Transcriber.transcribe")
def test_noramly_transcripted(transcribe):
    file = Path("file_test_normal")
    files_created.append(file)

    with open(file, "w") as f:
        f.write("test")

    transcribe.return_value.error = []
    utterance_1 = MagicMock()
    utterance_1.return_value.text = "AAAA"
    utterance_1.return_value.speaker = "A"
    utterance_2 = MagicMock()
    utterance_2.return_value.text = "BBBB"
    utterance_2.return_value.speaker = "B"
    transcribe.return_value.utterances = [
        utterance_1.return_value,
        utterance_2.return_value,
    ]

    transcript = transcribe_audio(file)

    assert transcript[0] == (
        "A",
        "AAAA",
    )
    assert transcript[1] == (
        "B",
        "BBBB",
    )
