#!/usr/bin/env python3
"""Locate the companion app; preserve arguments, output and exit status."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def app_root() -> Path:
    override = os.environ.get("FFKB_APP_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    skill = Path(__file__).resolve().parents[1]
    marker = skill / "installation.json"
    if marker.is_file():
        return Path(json.loads(marker.read_text())["app_root"])
    return skill.parents[1]


def main() -> int:
    try:
        root = app_root()
        entry = root / "ffkb.py"
        if not entry.is_file():
            raise OSError(
                f"Cannot find {entry}; set FFKB_APP_ROOT to the knowledge application's folder"
            )
        return subprocess.run(
            [sys.executable, str(entry), *sys.argv[1:]], check=False
        ).returncode
    except (OSError, ValueError, KeyError) as exc:
        print(f"flutter-flame-engineering: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
