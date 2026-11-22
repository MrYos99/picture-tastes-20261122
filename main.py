#!/usr/bin/env python3
"""Torn fried chicken — picture-tastes entry.

Reads the locked ``entry.jpg`` from this repository root (golden crispy
fried chicken torn in two halves, white shredded meat exposed, steam
rising from the tear), checks that it is a complete JPEG of exactly
1024x1024 pixels and no more than 1,048,576 bytes, then copies its bytes
unchanged to ``/output/entry.png``.

Python 3.13, standard library only, no network access. The output file
keeps the ``.png`` name the bounty harness expects, but its contents are
the original JPEG bytes, byte for byte.

Exit code 0 means every check passed and the copy is verified identical;
exit code 1 means a check failed, with the reason printed on stderr.
"""

from __future__ import annotations

import hashlib
import struct
import sys
from pathlib import Path

SOURCE_NAME = "entry.jpg"
TARGET_NAME = "entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_SIZE_BYTES = 1_048_576
JPEG_START = b"\xff\xd8"
JPEG_END = b"\xff\xd9"


class EntryError(RuntimeError):
    """Raised when the source image fails any acceptance check."""


def sha256_hex(blob: bytes) -> str:
    """Return the lowercase hex SHA-256 digest of *blob*."""
    return hashlib.sha256(blob).hexdigest()


def jpeg_dimensions(blob: bytes) -> tuple[int, int]:
    """Scan JPEG markers for the first SOF frame and return (width, height).

    Walks the marker segments from the start of the file; the frame header
    (SOF0/SOF1/SOF2) stores height then width as two big-endian shorts.
    Raises EntryError if no frame header is found before the scan data.
    """
    offset = 2  # skip the SOI marker (FFD8)
    while offset + 4 <= len(blob):
        if blob[offset] != 0xFF:
            offset += 1
            continue
        marker = blob[offset + 1]
        if marker in (0xC0, 0xC1, 0xC2):  # baseline / extended / progressive
            height, width = struct.unpack_from(">HH", blob, offset + 5)
            return width, height
        if marker == 0xDA:  # start of scan: no frame header follows
            break
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            offset += 2  # standalone markers carry no length field
            continue
        segment_len = struct.unpack_from(">H", blob, offset + 2)[0]
        offset += 2 + segment_len
    raise EntryError("no JPEG frame header (SOF) found")


def accept_source(blob: bytes) -> tuple[int, int]:
    """Run every acceptance check on the source bytes; return (w, h)."""
    if not blob.startswith(JPEG_START):
        raise EntryError("source does not start with JPEG SOI (FFD8)")
    if not blob.endswith(JPEG_END):
        raise EntryError("source does not end with JPEG EOI (FFD9)")
    if len(blob) > MAX_SIZE_BYTES:
        raise EntryError(
            f"source is {len(blob)} bytes, over the {MAX_SIZE_BYTES} limit"
        )
    width, height = jpeg_dimensions(blob)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise EntryError(
            f"source is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    return width, height


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    source_path = repo_root / SOURCE_NAME
    output_dir = Path("/output")
    output_path = output_dir / TARGET_NAME

    try:
        blob = source_path.read_bytes()
    except OSError as exc:
        print(f"error: cannot read {source_path}: {exc}", file=sys.stderr)
        return 1

    try:
        width, height = accept_source(blob)
    except EntryError as exc:
        print(f"error: {source_path} rejected: {exc}", file=sys.stderr)
        return 1

    source_digest = sha256_hex(blob)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(blob)

    # Re-read the copy and prove it is byte-identical to the source.
    written = output_path.read_bytes()
    if sha256_hex(written) != source_digest:
        print("error: output digest differs from source", file=sys.stderr)
        return 1

    print(
        f"ok: {SOURCE_NAME} -> {output_path} "
        f"({width}x{height} JPEG, {len(blob)} bytes, "
        f"sha256={source_digest})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
