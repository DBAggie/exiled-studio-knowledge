#!/usr/bin/env python3
"""Economy refresh (plan D4 rule 2, D7): one low-volume snapshot of a PoE1 league from
poe.ninja's supported economy-overview endpoints (https://poe.ninja/docs/api).

    python tools/refresh/economy.py [--league <id>] [--date YYYY-MM-DD] [--patch 3.30.0]

- Requests are sequential, with a pause between them, cached in local/refresh-cache/ with
  ETags (conditional requests), and send the User-Agent in REFRESH_USER_AGENT (poe.ninja asks
  for one that names the app and a contact; the default names only the app).
- Only the fields a price answer needs are kept: no icons, mod text, or flavour text.
- Writes plugins/poe1-expert/skills/poe1-economy/snapshots/<league-slug>/<date>.json with the
  knowledge header. Never commits; the scheduled task opens a PR for review (plan D7).
Standard library only. Exit 0 written, 1 a request failed, 2 usage.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://poe.ninja/poe1/api/economy"
CACHE = ROOT / "local" / "refresh-cache"
OUT = ROOT / "plugins" / "poe1-expert" / "skills" / "poe1-economy" / "snapshots"
UA = os.environ.get("REFRESH_USER_AGENT", "exiled-studio-knowledge-refresh/0.1")
PAUSE_S = 2.0

EXCHANGE_TYPES = ["Currency", "Fragment", "Scarab", "DivinationCard", "Essence", "Fossil", "Oil", "Omen"]
ITEM_TYPES = [
    "UniqueWeapon", "UniqueArmour", "UniqueAccessory", "UniqueFlask", "UniqueJewel",
    "SkillGem", "ClusterJewel",
]
ITEM_FIELDS = (
    "name", "baseType", "itemClass", "variant", "links", "gemLevel", "gemQuality", "corrupted",
    "mapTier", "levelRequired", "chaosValue", "divineValue", "listingCount",
)


def get(path: str, params: dict) -> object:
    url = f"{BASE}/{path}" + (f"?{urllib.parse.urlencode(params)}" if params else "")
    CACHE.mkdir(parents=True, exist_ok=True)
    key = CACHE / hashlib.sha256(url.encode()).hexdigest()[:24]
    headers = {"User-Agent": UA, "Accept": "application/json"}
    meta = key.with_suffix(".etag")
    if meta.exists() and key.with_suffix(".json").exists():
        headers["If-None-Match"] = meta.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            key.with_suffix(".json").write_bytes(body)
            if r.headers.get("ETag"):
                meta.write_text(r.headers["ETag"], encoding="utf-8")
    except urllib.error.HTTPError as e:
        if e.code != 304:
            raise
        body = key.with_suffix(".json").read_bytes()
    time.sleep(PAUSE_S)
    return json.loads(body)


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def exchange(league: str, kind: str) -> tuple[list[dict], object, object]:
    data = get("exchange/current/overview", {"league": league, "type": kind})
    named = (data.get("core") or {}).get("items", []) + (data.get("items") or [])
    names = {i.get("id"): i.get("name") for i in named}
    rows = []
    for line in data.get("lines", []):
        rows.append({
            "id": line.get("id"),
            "name": names.get(line.get("id"), line.get("id")),
            "value": line.get("primaryValue"),
            "volume": line.get("volumePrimaryValue"),
        })
    return rows, (data.get("core") or {}).get("primary"), (data.get("core") or {}).get("rates")


MIN_LISTINGS = {"SkillGem": 5}


def items(league: str, kind: str) -> list[dict]:
    data = get("stash/current/item/overview", {"league": league, "type": kind})
    floor = MIN_LISTINGS.get(kind, 0)
    return [
        {k: line[k] for k in ITEM_FIELDS if line.get(k) not in (None, "", [])}
        for line in data.get("lines", [])
        if (line.get("listingCount") or 0) >= floor
    ]


def dump(snap: dict) -> str:
    """One row per line: small diffs between refreshes, still valid JSON."""
    nl = "\n"

    def rows(lines: list[dict]) -> str:
        body = ("," + nl).join("   " + json.dumps(r, ensure_ascii=False) for r in lines)
        return "[" + nl + body + nl + "  ]" if lines else "[]"

    parts = [' "header": ' + json.dumps(snap["header"], ensure_ascii=False)]
    for k in ("league_id", "fetched_utc", "min_listings"):
        parts.append(f' "{k}": {json.dumps(snap[k])}')
    ex = ("," + nl).join(
        f'  "{k}": {{"primary": {json.dumps(v["primary"])}, "rates": {json.dumps(v["rates"])}, "lines": {rows(v["lines"])}}}'
        for k, v in snap["exchange"].items()
    )
    it = ("," + nl).join(f'  "{k}": {rows(v)}' for k, v in snap["items"].items())
    parts.append(' "exchange": {' + nl + ex + nl + " }")
    parts.append(' "items": {' + nl + it + nl + " }")
    return "{" + nl + ("," + nl).join(parts) + nl + "}" + nl


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--league", help="league id from poe.ninja (default: the first, the current challenge league)")
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).date().isoformat(), help="UTC date (default: today in UTC)")
    ap.add_argument("--patch", default="3.30.0")
    args = ap.parse_args(argv[1:])

    leagues = get("leagues", {})
    if not leagues:
        print("no leagues returned", file=sys.stderr)
        return 1
    league = next((l for l in leagues if l["id"] == args.league), None) if args.league else leagues[0]
    if league is None:
        print(f"unknown league {args.league!r}; known: {[l['id'] for l in leagues]}", file=sys.stderr)
        return 2

    snap: dict = {
        "header": {
            "game": "poe1",
            "patch": args.patch,
            "league": league["name"],
            "as_of": args.date,
            "sources": ["https://poe.ninja/docs/api"],
            "verification": "unverified",
            "status": "current",
        },
        "league_id": league["id"],
        "fetched_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "min_listings": MIN_LISTINGS,
        "exchange": {},
        "items": {},
    }
    try:
        for kind in EXCHANGE_TYPES:
            rows, primary, rates = exchange(league["id"], kind)
            snap["exchange"][kind] = {"primary": primary, "rates": rates, "lines": rows}
        for kind in ITEM_TYPES:
            snap["items"][kind] = items(league["id"], kind)
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"request failed: {e}", file=sys.stderr)
        return 1

    out = OUT / slug(league["name"]) / f"{args.date}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap, indent=1, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8", newline="\n")
    counts = {k: len(v["lines"]) for k, v in snap["exchange"].items()} | {k: len(v) for k, v in snap["items"].items()}
    print(json.dumps({"written": out.relative_to(ROOT).as_posix(), "league": league["name"], "counts": counts}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
