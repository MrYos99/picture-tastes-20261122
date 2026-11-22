#!/usr/bin/env python3
"""Torn fried chicken — picture-tastes bounty entry.

Reads the locked entry image (``entry.jpg``) from the repository root,
checks it is a whole 1024x1024 JPEG within the 1 MiB size limit, and
copies its bytes unchanged to ``/output/entry.png``. The output is then
re-read and its SHA-256 compared against the source, so the file that
leaves the repo is provably the exact image John picked.

Verified image contract (checked before the entry was sealed):
``entry.jpg`` is a whole 1024x1024 JPEG of 168,486 bytes, sha256
70d8bcb1a5682e8f9ba5cd8c5bc525af87130dd4baf13224abf15717c5046707,
and ``/output/entry.png`` must be byte-identical to it.

Exits 0 on success and 1 on any failed check, with the reason on
stderr. Standard library only; no network access.
"""

from __future__ import annotations

import hashlib
import shutil
import struct
import sys
from pathlib import Path

SOURCE_NAME = "entry.jpg"
OUTPUT_PATH = Path("/output/entry.png")
MAX_BYTES = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024

JPEG_START = b"\xff\xd8"
JPEG_END = b"\xff\xd9"

# Markers whose segments carry a frame header (baseline / progressive).
FRAME_MARKERS = {0xC0, 0xC1, 0xC2}


def sha256_hex(data: bytes) -> str:
    """Return the lowercase hex SHA-256 digest of ``data``."""
    return hashlib.sha256(data).hexdigest()


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Extract (width, height) from the first JPEG frame header.

    Walks the marker segments after the SOI marker until a frame
    (SOF0/SOF1/SOF2) marker is found; its payload stores the height
    and width as two big-endian 16-bit values.
    """
    pos = 2  # skip the SOI marker
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            raise ValueError("malformed JPEG: expected a marker")
        marker = data[pos + 1]
        if marker in FRAME_MARKERS:
            height, width = struct.unpack(">HH", data[pos + 5 : pos + 9])
            return width, height
        if marker == 0xD8:  # stray SOI — advance one byte and keep looking
            pos += 1
            continue
        segment_len = struct.unpack(">H", data[pos + 2 : pos + 4])[0]
        pos += 2 + segment_len
    raise ValueError("no JPEG frame header found")


def check_image(data: bytes, label: str) -> tuple[int, int]:
    """Validate the image bytes and return their dimensions."""
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"{label}: {len(data)} bytes exceeds the {MAX_BYTES} byte limit"
        )
    if not data.startswith(JPEG_START):
        raise ValueError(f"{label}: missing JPEG SOI marker (FFD8)")
    if not data.endswith(JPEG_END):
        raise ValueError(f"{label}: missing JPEG EOI marker (FFD9)")
    width, height = jpeg_dimensions(data)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            f"{label}: {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    return width, height


def main() -> int:
    source_path = Path(__file__).resolve().parent / SOURCE_NAME

    try:
        source_bytes = source_path.read_bytes()
    except FileNotFoundError:
        print(f"error: {source_path} not found", file=sys.stderr)
        return 1

    try:
        check_image(source_bytes, SOURCE_NAME)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, OUTPUT_PATH)

    output_bytes = OUTPUT_PATH.read_bytes()
    if sha256_hex(output_bytes) != sha256_hex(source_bytes):
        print("error: output digest differs from source", file=sys.stderr)
        return 1

    width, height = jpeg_dimensions(output_bytes)
    print(
        f"ok: {SOURCE_NAME} -> {OUTPUT_PATH} "
        f"({width}x{height} JPEG, {len(output_bytes)} bytes, "
        f"sha256 {sha256_hex(output_bytes)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
