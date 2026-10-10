#!/usr/bin/env python3
"""Read original file metadata or one upload chunk. No network or data execution."""
import argparse
import base64
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--offset", type=int, help="Omit for filename, byte length and SHA-256 only")
    parser.add_argument("--max-bytes", type=int, default=65536)
    args = parser.parse_args()
    if not 1 <= args.max_bytes <= 65536 or (args.offset is not None and args.offset < 0):
        parser.error("Use a nonnegative offset and 1–65536 bytes")
    with args.file.open("rb") as handle:
        if args.offset is None:
            hasher = hashlib.sha256()
            size = 0
            while chunk := handle.read(1024 * 1024):
                hasher.update(chunk)
                size += len(chunk)
            result = {"file_name": args.file.name, "size_bytes": size, "expected_sha256": hasher.hexdigest()}
        else:
            handle.seek(args.offset)
            data = handle.read(args.max_bytes)
            if not data:
                parser.error("Offset is outside this file")
            result = {"offset": args.offset, "content_base64": base64.b64encode(data).decode(),
                      "next_offset": args.offset + len(data)}
    print(json.dumps(result))


if __name__ == "__main__":
    main()
