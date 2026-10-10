#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

from spec_utils import sha256


EXPECTED_TEMPLATE_SHA256 = "3e47b52a41be6f60710513bc7ddedd73b1e3cde5dc6fa150a9bb9c4533384f1f"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    if not slug:
        raise ValueError("model name must contain at least one letter or digit")
    return slug


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy the protected MTS template into a project.")
    parser.add_argument("model", help="Model or project name used for the default directory slug")
    parser.add_argument("--root", default=".", help="Project root (default: current directory)")
    parser.add_argument("--output", help="Explicit output file instead of specifications/<slug>/mts.md")
    args = parser.parse_args()
    skill_root = Path(__file__).resolve().parent.parent
    template = skill_root / "assets" / "master-template.md"
    actual_hash = sha256(template)
    if actual_hash != EXPECTED_TEMPLATE_SHA256:
        parser.error(f"protected template integrity check failed: {actual_hash}")
    root = Path(args.root).expanduser().resolve()
    output = Path(args.output).expanduser().resolve() if args.output else root / "specifications" / slugify(args.model) / "mts.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output.open("xb") as handle:
            handle.write(template.read_bytes())
    except FileExistsError:
        parser.error(f"refusing to overwrite existing document: {output}")
    os.chmod(output, 0o644)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
