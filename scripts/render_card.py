#!/usr/bin/env python3
"""Render a deterministic 1200×630 public kit from one sealed Bout."""

from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, NoReturn
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
CARD_WIDTH = 1200
CARD_HEIGHT = 630
SIZE_META = '<meta name="bout-card-size" content="1200x630">'


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot read JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain a JSON object")
    return value


def discover_chrome(explicit: str | None) -> str:
    candidates = [
        explicit,
        os.environ.get("BOUT_CHROME"),
        "google-chrome",
        "chromium",
        "chromium-browser",
    ]
    for candidate in candidates:
        if candidate and shutil.which(candidate):
            return shutil.which(candidate) or candidate
    fail("Chrome/Chromium not found; set BOUT_CHROME to its executable")


def file_url(path: Path) -> str:
    return "file://" + quote(str(path.resolve()))


def png_size(path: Path) -> tuple[int, int]:
    try:
        with path.open("rb") as image:
            header = image.read(24)
    except OSError as exc:
        fail(f"cannot read rendered PNG {path}: {exc}")
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"renderer did not produce a PNG: {path}")
    return struct.unpack(">II", header[16:24])


def screenshot(chrome: str, source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="bout-chrome-") as profile:
        command = [
            chrome,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-background-networking",
            "--disable-default-apps",
            "--disable-extensions",
            "--disable-sync",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
            "--force-device-scale-factor=1",
            f"--window-size={CARD_WIDTH},{CARD_HEIGHT}",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=1000",
            f"--user-data-dir={profile}",
            f"--screenshot={target.resolve()}",
            file_url(source),
        ]
        process = subprocess.run(command, text=True, capture_output=True, check=False)
    if process.returncode:
        detail = (process.stderr or process.stdout).strip()
        fail(f"Chrome failed rendering {source}: {detail}")
    dimensions = png_size(target)
    if dimensions != (CARD_WIDTH, CARD_HEIGHT):
        fail(f"{target} is {dimensions[0]}×{dimensions[1]}, expected 1200×630")


def validate_template(path: Path) -> str:
    try:
        template = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read template {path}: {exc}")
    if SIZE_META not in template:
        fail(f"{path} is missing the 1200×630 card-size metadata")
    if "width:1200px" not in template or "height:630px" not in template:
        fail(f"{path} must declare a fixed 1200×630 frame")
    return template


def fill(template: str, values: dict[str, str]) -> str:
    for token, value in values.items():
        template = template.replace("{{" + token + "}}", value)
    if "{{" in template or "}}" in template:
        fail("card template contains an unresolved token")
    return template


def card_values(result: dict[str, Any]) -> dict[str, str]:
    fighters = result["fighters"]
    if len(fighters) != 2:
        fail("public kit requires exactly two fighters")
    left, right = fighters
    winner_id = result["decision"]["winner"]
    winner = next((fighter for fighter in fighters if fighter["id"] == winner_id), None)
    headline = f"{winner['name']} wins" if winner else "Decision pending"
    show = result.get("show", {})
    captions = show.get("fighter_captions", {})
    criterion = result["decision"]["tiebreak"]["criterion"].replace("_", " ")
    return {
        "BOUT_ID": html.escape(result["bout_id"]),
        "LANE": html.escape(result["lane"]),
        "HEADLINE": html.escape(headline),
        "SHOW_TITLE": html.escape(show.get("title", "Sealed dual meet")),
        "RUBRIC_SCORE": "–".join(str(fighter["passes"]) for fighter in fighters),
        "TIEBREAK": html.escape(criterion),
        "LEFT_NAME": html.escape(left["name"]),
        "RIGHT_NAME": html.escape(right["name"]),
        "LEFT_CAPTION": html.escape(captions.get(left["id"], f"{left['passes']} rubric passes")),
        "RIGHT_CAPTION": html.escape(captions.get(right["id"], f"{right['passes']} rubric passes")),
        "LEFT_WINNER": "winner" if left["id"] == winner_id else "",
        "RIGHT_WINNER": "winner" if right["id"] == winner_id else "",
        "ROAST": html.escape(show.get("roast", result["decision"]["reason"].replace("_", " "))),
    }


def dry_run(bout_path: Path, cards_dir: Path | None) -> dict[str, Any]:
    bout = load_json(bout_path)
    for key in ("id", "lane", "fighters"):
        if key not in bout:
            fail(f"bout is missing required field: {key}")
    if not isinstance(bout["fighters"], list) or len(bout["fighters"]) != 2:
        fail("bout must declare exactly two fighters")
    validate_template(ROOT / "cards" / "side-by-side.html")
    validate_template(ROOT / "cards" / "result-card.html")
    destination = (cards_dir or bout_path.parent / "cards").resolve()
    return {
        "bout_id": bout["id"],
        "dry_run": True,
        "dimensions": f"{CARD_WIDTH}x{CARD_HEIGHT}",
        "cards_dir": str(destination),
        "templates_valid": True,
    }


def render(bout_path: Path, cards_dir: Path | None, chrome_arg: str | None) -> dict[str, Any]:
    bout_path = bout_path.resolve()
    generated_dir = bout_path.parent / "generated"
    judge = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "judge"), str(bout_path), "--output", str(generated_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if judge.returncode:
        fail(f"judge failed: {(judge.stderr or judge.stdout).strip()}")
    summary = json.loads(judge.stdout)
    result_path = Path(summary["result_json"])
    result = load_json(result_path)
    destination = (cards_dir or bout_path.parent / "cards").resolve()
    destination.mkdir(parents=True, exist_ok=True)
    chrome = discover_chrome(chrome_arg)

    fighter_assets: dict[str, str] = {}
    for fighter in result["fighters"]:
        source = Path(fighter["artifact"]["path"])
        if source.suffix.lower() not in {".html", ".htm"}:
            continue
        target = destination / f"{source.stem}.png"
        screenshot(chrome, source, target)
        fighter_assets[fighter["id"]] = str(target)
    if len(fighter_assets) != 2:
        fail("side-by-side rendering currently requires two HTML fighter artifacts")

    values = card_values(result)
    left, right = result["fighters"]
    side_template = validate_template(ROOT / "cards" / "side-by-side.html")
    side_values = {
        **values,
        "LEFT_ASSET": html.escape(Path(fighter_assets[left["id"]]).name, quote=True),
        "RIGHT_ASSET": html.escape(Path(fighter_assets[right["id"]]).name, quote=True),
    }
    side_html = destination / "side-by-side.html"
    side_png = destination / "side-by-side.png"
    side_html.write_text(fill(side_template, side_values), encoding="utf-8")
    screenshot(chrome, side_html, side_png)

    result_template = validate_template(ROOT / "cards" / "result-card.html")
    result_html = destination / "result.html"
    result_png = destination / "result.png"
    result_html.write_text(fill(result_template, values), encoding="utf-8")
    screenshot(chrome, result_html, result_png)

    public_kit = {
        "dimensions": f"{CARD_WIDTH}x{CARD_HEIGHT}",
        "fighter_assets": fighter_assets,
        "side_by_side_html": str(side_html),
        "side_by_side_png": str(side_png),
        "result_card_html": str(result_html),
        "result_card_png": str(result_png),
        "rendered": True,
    }
    result["artifacts"]["public_kit"] = public_kit
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return {"bout_id": result["bout_id"], "result_json": str(result_path), "public_kit": public_kit}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Judge a Bout and render its deterministic 1200×630 public kit"
    )
    parser.add_argument("bout", type=Path, help="path to bout.json")
    parser.add_argument("--cards-dir", type=Path, help="override the public-kit output directory")
    parser.add_argument("--chrome", help="Chrome/Chromium executable (or set BOUT_CHROME)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate inputs/templates and print the plan without judging or rendering",
    )
    args = parser.parse_args()
    try:
        output = (
            dry_run(args.bout.resolve(), args.cards_dir)
            if args.dry_run
            else render(args.bout, args.cards_dir, args.chrome)
        )
    except (RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"render-card: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
