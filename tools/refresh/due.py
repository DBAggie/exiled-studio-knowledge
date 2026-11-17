#!/usr/bin/env python3
"""Say which economy snapshots are due for a refresh. Reads only this repository; it makes
no request. Refreshes run by hand (REVIEW-QUEUE Q7), so run this to see when to run one.

    python tools/refresh/due.py [--max-age 7] [--today YYYY-MM-DD]

For each league folder under snapshots/, prints the newest snapshot's date and age in days.
A league is `due` when its newest snapshot is older than --max-age days (use 2 in a
league's first week, 7 to 14 after; plan D7). Leagues whose newest snapshot is marked
`historical` are listed and never due. Exit 0 nothing due, 1 something due.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

SNAPSHOTS = Path(__file__).resolve().parents[2] / "plugins" / "poe1-expert" / "skills" / "poe1-economy" / "snapshots"


def status_of(path: Path) -> str:
    try:
        with path.open(encoding="utf-8") as f:
            head = f.read(2000)
    except OSError:
        return "current"
    m = re.search(r'"status":\s*"([a-z]+)"', head)
    return m.group(1) if m else "current"


def leagues(root: Path, today: dt.date, max_age: int) -> list[dict]:
    out = []
    for folder in sorted(p for p in root.iterdir() if p.is_dir()) if root.exists() else []:
        dated = sorted(p for p in folder.glob("*.json") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.stem))
        if not dated:
            continue
        newest = dated[-1]
        age = (today - dt.date.fromisoformat(newest.stem)).days
        status = status_of(newest)
        out.append({"league": folder.name, "newest": newest.stem, "age_days": age, "status": status,
                    "due": status != "historical" and age > max_age})
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-age", type=int, default=7)
    ap.add_argument("--today", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    ap.add_argument("--root", default=str(SNAPSHOTS), help=argparse.SUPPRESS)
    args = ap.parse_args(argv[1:])
    rows = leagues(Path(args.root), dt.date.fromisoformat(args.today), args.max_age)
    if not rows:
        print("no snapshots found")
        return 1
    for r in rows:
        mark = "historical" if r["status"] == "historical" else ("DUE" if r["due"] else "ok")
        print(f"{r['league']:24} newest {r['newest']}  {r['age_days']:3} day(s) old  {mark}")
    print(json.dumps({"due": [r["league"] for r in rows if r["due"]]}))
    return 1 if any(r["due"] for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
