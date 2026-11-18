#!/usr/bin/env python3
"""news-image-20261118 entry (Python 3.13, standard library only).

The entry image is the pre-rendered front page entry.png beside this file:
a one-page newspaper summary of Wednesday 18 November 2026 world news,
rendered at build time by gen_image.py (Pillow + system fonts) from wire
reports of the day. The graded program does nothing but copy that image
to the output directory, so it needs no network and is deterministic:
two runs write the same bytes.

Run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    """Copy the pre-rendered front page to the output directory."""
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT / "entry.png")


if __name__ == "__main__":
    main()
