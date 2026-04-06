#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def check_ffmpeg() -> None:
    """Ensure ffmpeg is installed and available on PATH."""
    if shutil.which("ffmpeg") is None:
        print(
            "Error: ffmpeg is not installed or not on your PATH.\n"
            "Install it on macOS with:\n"
            "  brew install ffmpeg",
            file=sys.stderr,
        )
        sys.exit(1)


def convert_file(opus_file: Path, bitrate: str, overwrite: bool) -> None:
    """Convert one OPUS file to MP3."""
    mp3_file = opus_file.with_suffix(".mp3")

    if mp3_file.exists() and not overwrite:
        print(f"Skipping (already exists): {mp3_file.name}")
        return

    cmd = [
        "ffmpeg",
        "-i",
        str(opus_file),
        "-vn",
        "-codec:a",
        "libmp3lame",
        "-b:a",
        bitrate,
    ]

    if overwrite:
        cmd.append("-y")
    else:
        cmd.append("-n")

    cmd.append(str(mp3_file))

    print(f"Converting: {opus_file.name} -> {mp3_file.name}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"Failed: {opus_file.name}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    else:
        print(f"Done: {mp3_file.name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert all .opus files in a folder to .mp3 using ffmpeg."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder containing .opus files (default: current folder)",
    )
    parser.add_argument(
        "--bitrate",
        default="192k",
        help="MP3 bitrate, e.g. 128k, 192k, 320k (default: 192k)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing .mp3 files",
    )

    args = parser.parse_args()

    check_ffmpeg()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        print(f"Error: not a folder: {folder}", file=sys.stderr)
        sys.exit(1)

    opus_files = sorted(folder.glob("*.opus"))
    if not opus_files:
        print(f"No .opus files found in: {folder}")
        return

    print(f"Found {len(opus_files)} .opus file(s) in: {folder}")
    for opus_file in opus_files:
        convert_file(opus_file, args.bitrate, args.overwrite)


if __name__ == "__main__":
    main()
    