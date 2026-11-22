#!/usr/bin/env python3
"""Picture-tastes entry: emit the locked fried-chicken image.

The picture itself was chosen by the entrant before this program was
written and lives in the repository as entry.jpg. The grading sandbox
has no network and only the standard library, so this program does
nothing creative at run time: it proves the stored picture is a whole
1024x1024 JPEG inside the 1 MiB cap, then copies its bytes unchanged
to /output/entry.png and proves the copy byte-for-byte.

Same bytes in, same bytes out, every run.
"""

import hashlib
import os
import struct
import sys

EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
BYTE_CAP = 1_048_576
SOURCE_NAME = "entry.jpg"


def frame_dimensions(blob):
    """Scan JPEG markers for the SOF frame; return (width, height)."""
    pos = 2  # skip the SOI marker
    while pos + 9 <= len(blob):
        if blob[pos] != 0xFF:
            pos += 1
            continue
        marker = blob[pos + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height = struct.unpack(">H", blob[pos + 5:pos + 7])[0]
            width = struct.unpack(">H", blob[pos + 7:pos + 9])[0]
            return width, height
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        segment = struct.unpack(">H", blob[pos + 2:pos + 4])[0]
        pos += 2 + segment
    return None


def validate(blob):
    """Refuse anything that is not a whole 1024x1024 JPEG under the cap."""
    if len(blob) > BYTE_CAP:
        sys.exit("entry image is %d bytes, over the 1 MiB cap" % len(blob))
    if blob[:3] != b"\xff\xd8\xff":
        sys.exit("entry image does not start with the JPEG SOI marker")
    if blob[-2:] != b"\xff\xd9":
        sys.exit("entry image does not end with the JPEG EOI marker")
    dims = frame_dimensions(blob)
    if dims is None:
        sys.exit("no JPEG frame header found in entry image")
    if dims != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        sys.exit("entry image is %dx%d, expected %dx%d"
                 % (dims[0], dims[1], EXPECTED_WIDTH, EXPECTED_HEIGHT))
    return dims


def run():
    repo = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(repo, SOURCE_NAME), "rb") as handle:
        blob = handle.read()
    width, height = validate(blob)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(blob)
    with open(target, "rb") as handle:
        copied = handle.read()
    if hashlib.sha256(copied).hexdigest() != hashlib.sha256(blob).hexdigest():
        sys.exit("copied image differs from the stored image")
    validate(copied)
    print("wrote %s: JPEG %dx%d, %d bytes, sha256 %s..."
          % (target, width, height, len(blob),
             hashlib.sha256(blob).hexdigest()[:16]))


if __name__ == "__main__":
    run()
