#!/usr/bin/env python3
from pathlib import Path
import sys

try:
    from mutagen.id3 import ID3, ID3NoHeaderError
except ImportError:
    print("Error: mutagen is not installed.")
    print("Install it with: pip install mutagen")
    sys.exit(1)


def remove_mp3_metadata(folder: Path) -> None:
    mp3_files = list(folder.glob("*.mp3"))

    if not mp3_files:
        print("No .mp3 files found in the current folder.")
        return

    for mp3_file in mp3_files:
        try:
            try:
                tags = ID3(mp3_file)
                tags.delete(mp3_file)
                print(f"Removed metadata: {mp3_file.name}")
            except ID3NoHeaderError:
                print(f"No ID3 metadata found: {mp3_file.name}")
        except Exception as e:
            print(f"Failed to process {mp3_file.name}: {e}")


if __name__ == "__main__":
    current_folder = Path.cwd()
    remove_mp3_metadata(current_folder)
    