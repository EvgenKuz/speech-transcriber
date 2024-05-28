from os import PathLike
from pathlib import Path

import assemblyai as aai

from errors import AudioBiggerThanTwoPointTwoGigabytes, TranscribingError
from settings import load_toml_settings

eps = 1e-9


def create_transcriber() -> tuple[aai.Transcriber, aai.TranscriptionConfig]:
    aai.settings.api_key = load_toml_settings()["api"]["tokens"]["assemblyai"]

    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True, language_code="ru")

    return transcriber, config


def transcribe_audio(audio_location: PathLike) -> list[tuple[str | None, str]]:
    transcriber, config = create_transcriber()
    audio_location = Path(audio_location)

    if not audio_location.exists() or not audio_location.is_file():
        raise FileNotFoundError()

    file_size_in_gb = audio_location.stat().st_size / 1024 / 1024 / 1024

    if file_size_in_gb > 2.2 + eps:
        raise AudioBiggerThanTwoPointTwoGigabytes(
            f"Size of file is {file_size_in_gb} GB, which is more than 2.2 GB"
        )

    transcript = transcriber.transcribe(str(audio_location), config)

    if transcript.error:
        raise TranscribingError(transcript.error)

    return [
        (utterance.speaker, utterance.text)
        for utterance in (
            transcript.utterances if transcript.utterances is not None else []
        )
    ]


def save_transcribed_to_file(
    utterances: list[tuple[str | None, str]],
    output_file: PathLike | str,
    overwrite: bool = False,
):
    output_file = Path(output_file)
    if output_file.exists() and (not overwrite or output_file.is_dir()):
        raise FileExistsError(f"File {output_file} already exists")

    with open(output_file, "w") as file:
        file.writelines(
            [
                f"Speaker {speaker if speaker is not None else 'None'}: {utterance}\n\n"
                for speaker, utterance in utterances
            ]
        )
