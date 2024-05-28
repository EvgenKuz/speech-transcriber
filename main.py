from pathlib import Path

from transcribe_audio import save_transcribed_to_file, transcribe_audio

eps = 1e-9


def main():
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
