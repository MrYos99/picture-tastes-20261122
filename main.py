#!/usr/bin/env python3
"""Torn fried chicken — picture-tastes bounty entry.

Reads ``entry.jpg`` from this repository root, checks that it is a whole
JPEG of exactly 1024x1024 pixels and no larger than 1 MiB, then copies its
bytes unchanged to ``/output/entry.png`` and re-verifies the copy by
comparing SHA-256 digests. The output keeps the ``.png`` name the bounty
harness expects, while its contents stay the original JPEG bytes.

Standard library only. No network access. Python 3.13. Exit code 0 means
every gate passed and the copy is verified identical; any failure prints
its reason to stderr and exits non-zero.
"""

from __future__ import annotations

import hashlib
import os
import struct
import sys

SOURCE_NAME = "entry.jpg"
OUTPUT_PATH = "/output/entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1_048_576


def fail(message: str) -> "SystemExit":
    """Report a failed gate and stop with a non-zero exit code."""
    print(f"FAIL: {message}", file=sys.stderr)
    return SystemExit(1)


def read_jpeg_dimensions(blob: bytes) -> tuple[int, int]:
    """Return (width, height) from the first SOF marker in a JPEG blob."""
    cursor = 2  # skip the SOI marker (FFD8)
    while cursor + 1 < len(blob):
        if blob[cursor] != 0xFF:
            cursor += 1
            continue
        marker = blob[cursor + 1]
        if marker in (0xC0, 0xC1, 0xC2):  # baseline / progressive SOF
            height, width = struct.unpack_from(">HH", blob, cursor + 5)
            return width, height
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            cursor += 2
            continue
        segment_len = struct.unpack_from(">H", blob, cursor + 2)[0]
        cursor += 2 + segment_len
    raise ValueError("no SOF marker found")


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, SOURCE_NAME)

    with open(source_path, "rb") as handle:
        blob = handle.read()

    if len(blob) > MAX_BYTES:
        raise SystemExit(fail(f"entry.jpg is {len(blob)} bytes, over {MAX_BYTES}"))
    if not blob.startswith(b"\xff\xd8"):
        raise SystemExit(fail("entry.jpg does not start with JPEG magic FFD8"))
    if not blob.endswith(b"\xff\xd9"):
        raise SystemExit(fail("entry.jpg does not end with JPEG magic FFD9"))

    width, height = read_jpeg_dimensions(blob)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            fail(f"entry.jpg is {width}x{height}, expected "
                 f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")
        )

    source_hash = digest(blob)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(blob)

    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if digest(written) != source_hash:
        raise SystemExit(fail("output digest does not match source digest"))

    print(
        f"OK: {SOURCE_NAME} -> {OUTPUT_PATH} | "
        f"{width}x{height} JPEG | {len(blob)} bytes | sha256 {source_hash}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
