#!/usr/bin/env python3

from pathlib import Path
import re

# Match only:
#   GL1_001.mp3 ... GL9_999.mp3
# and NOT:
#   GL10_001.mp3, GL39_009.mp3, GL01_001.mp3
pattern = re.compile(r"^GL([1-9])_(\d{3})\.mp3$")

folder = Path(".")  # change this if needed, e.g. Path("/path/to/folder")

for path in folder.iterdir():
    if not path.is_file():
        continue

    m = pattern.match(path.name)
    if not m:
        continue

    gl_num = int(m.group(1))
    suffix = m.group(2)
    new_name = f"GL{gl_num:02d}_{suffix}.mp3"
    new_path = path.with_name(new_name)

    if new_path.exists():
        print(f"Skipping {path.name} -> {new_name} (target already exists)")
        continue

    print(f"Renaming {path.name} -> {new_name}")
    path.rename(new_path)
    