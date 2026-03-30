#!/usr/bin/env python3

from pathlib import Path
import re
import sys

PREVIEW = True
FOLDER = Path(".")

# Matches:
#   GL1_001.mp3
#   ABC9_004.wav
#   1_001.mp3
#   12_notes.txt
#
# Groups:
#   1 = optional non-digit prefix (may be empty)
#   2 = number to pad
#   3 = rest of filename after underscore
pattern = re.compile(r"^([^\d]*)(\d+)_(.+)$")

matches = []
width_by_prefix = {}

for path in FOLDER.iterdir():
    if not path.is_file():
        continue

    m = pattern.match(path.name)
    if not m:
        continue

    prefix, num_str, rest = m.groups()
    matches.append((path, prefix, num_str, rest))
    width_by_prefix[prefix] = max(width_by_prefix.get(prefix, 0), len(num_str))

if not matches:
    print("No matching numbered files found.")
    sys.exit(0)

renames = []

for path, prefix, num_str, rest in matches:
    target_width = width_by_prefix[prefix]

    if len(num_str) >= target_width:
        continue

    new_num = f"{int(num_str):0{target_width}d}"
    new_name = f"{prefix}{new_num}_{rest}"
    new_path = path.with_name(new_name)
    renames.append((path, new_path))

if not renames:
    print("Nothing needs renaming.")
    sys.exit(0)

conflicts = []
for old_path, new_path in renames:
    if new_path.exists() and new_path != old_path:
        conflicts.append((old_path.name, new_path.name))

if conflicts:
    print("Conflicts detected. No files were renamed:")
    for old_name, new_name in conflicts:
        print(f"  {old_name} -> {new_name} (target already exists)")
    sys.exit(1)

for old_path, new_path in renames:
    action = "Would rename" if PREVIEW else "Renaming"
    print(f"{action} {old_path.name} -> {new_path.name}")
    if not PREVIEW:
        old_path.rename(new_path)

if PREVIEW:
    print("Preview only. No files were renamed.")
else:
    print("Done.")
    