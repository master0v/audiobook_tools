#!/usr/bin/env bash
set -euo pipefail

root="$(pwd)"

# Move every file from subfolders into the current directory
find "$root" -mindepth 2 -type f | while IFS= read -r file; do
    base="$(basename "$file")"
    target="$root/$base"

    # If a file with the same name exists, add _1, _2, etc.
    if [[ -e "$target" ]]; then
        name="${base%.*}"
        ext=""
        if [[ "$base" == *.* && "$base" != .* ]]; then
            name="${base%.*}"
            ext=".${base##*.}"
        else
            name="$base"
        fi

        i=1
        while [[ -e "$root/${name}_$i$ext" ]]; do
            ((i++))
        done
        target="$root/${name}_$i$ext"
    fi

    mv "$file" "$target"
done

# Delete all now-empty subdirectories, deepest first
find "$root" -mindepth 1 -type d -empty -delete
