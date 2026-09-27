#!/usr/bin/env python3
"""DQ gate for Config Clash: require pre-kickoff hashes and material distinctness."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

MATERIAL_KEYS = [
    "name", "title", "description", "avatarShape", "avatarColor",
    "harness", "settings", "skills", "routines", "connectors", "memory",
]

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("seal", type=Path, help="pre-kickoff-seal.json")
    args = p.parse_args()
    base = args.seal.parent
    seal = json.loads(args.seal.read_text())
    corners = seal.get("corners") or {}
    if len(corners) != 2:
        print("DQ: seal must name exactly two corners", file=sys.stderr)
        return 2
    cores = []
    hashes = []
    for fid, info in corners.items():
        h = info.get("sha256")
        if not h or len(h) != 64:
            print(f"DQ: missing pre-kickoff hash for {fid}", file=sys.stderr)
            return 2
        man_path = base / info["manifest"]
        raw = man_path.read_text(encoding="utf-8")
        man = json.loads(raw)
        canon = json.dumps(man, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        dig = hashlib.sha256(canon.encode("utf-8")).hexdigest()
        if dig != h:
            print(f"DQ: hash mismatch for {fid}: seal={h} recomputed={dig}", file=sys.stderr)
            return 2
        core = {k: man.get(k) for k in MATERIAL_KEYS}
        cores.append(core)
        hashes.append(h)
    if hashes[0] == hashes[1]:
        print("DQ: identical pre-kickoff hashes", file=sys.stderr)
        return 2
    if cores[0] == cores[1]:
        print("DQ: identical material manifests", file=sys.stderr)
        return 2
    a = {k: v for k, v in cores[0].items() if k != "name"}
    b = {k: v for k, v in cores[1].items() if k != "name"}
    if a == b:
        print("DQ: rename theater (material equal excluding name)", file=sys.stderr)
        return 2
    print(json.dumps({"status": "ok", "hashes": hashes}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
