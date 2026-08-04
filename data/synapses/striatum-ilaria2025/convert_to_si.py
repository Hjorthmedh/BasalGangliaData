#!/usr/bin/env python3
"""Convert tau* fields (ms -> s) in JSON files, write results to a SI subfolder."""

import json
from pathlib import Path

INPUT_FOLDER = Path(".")  # change to your folder if needed

def convert_file(path: Path, out_dir: Path):
    with open(path) as f:
        d = json.load(f)

    for key, val in d.get("data", {}).items():
        if key.startswith("tau"):
            d["data"][key] = val / 1000.0  # ms -> s

    out_path = out_dir / (path.stem + "-SI.json")
    with open(out_path, "w") as f:
        json.dump(d, f, indent=2)

def main():
    out_dir = INPUT_FOLDER / "SI"
    out_dir.mkdir(exist_ok=True)

    for path in INPUT_FOLDER.glob("*.json"):
        convert_file(path, out_dir)
        print(f"Converted {path.name} -> SI/{path.stem}-SI.json")

if __name__ == "__main__":
    main()
