#!/usr/bin/env python3
"""Ship the pre-rendered 26 November 2026 front page.

This entry point does no drawing at all: the poster was rendered
offline by draw_poster.py and stored next to this file as entry.png.
All this script does is check that the bundled image is intact and
copy it, byte for byte, into the grading output directory.

Only the Python standard library is used, so nothing here depends on
external libraries, the network, or anything else that may be
missing from a minimal grading image.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
WANT_WIDTH = 1024
WANT_HEIGHT = 1024


def fail(message):
    print("error: %s" % message, file=sys.stderr)
    sys.exit(1)


def read_bundled_poster():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        fail("bundled poster not found: %s" % source)
    try:
        data = source.read_bytes()
    except OSError as exc:
        fail("cannot read bundled poster %s: %s" % (source, exc))
    return source, data


def check_poster(data):
    if len(data) < 33:
        fail("poster too short to be a PNG (%d bytes)" % len(data))
    if data[:8] != PNG_MAGIC:
        fail("poster does not start with the PNG signature")
    if len(data) >= MAX_BYTES:
        fail("poster is %d bytes, over the 1 MiB limit" % len(data))
    chunk_len, chunk_type = struct.unpack(">I4s", data[8:16])
    if chunk_type != b"IHDR" or chunk_len != 13:
        fail("first PNG chunk is not a 13-byte IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width != WANT_WIDTH or height != WANT_HEIGHT:
        fail("poster is %dx%d, expected %dx%d"
             % (width, height, WANT_WIDTH, WANT_HEIGHT))
    return width, height


def main():
    source, data = read_bundled_poster()
    width, height = check_poster(data)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = Path(out_dir) / "entry.png"
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    except OSError as exc:
        fail("cannot copy poster to %s: %s" % (target, exc))

    try:
        copied = target.read_bytes()
    except OSError as exc:
        fail("cannot re-read copied poster %s: %s" % (target, exc))
    if len(copied) != len(data):
        fail("copied poster is %d bytes, source is %d bytes"
             % (len(copied), len(data)))
    if copied[:8] != PNG_MAGIC:
        fail("copied poster does not start with the PNG signature")
    if hashlib.sha256(copied).hexdigest() != hashlib.sha256(data).hexdigest():
        fail("copied poster hash differs from the bundled poster")

    print("ok: copied entry.png (%dx%d, %d bytes, sha256 %s) to %s"
          % (width, height, len(copied),
             hashlib.sha256(copied).hexdigest(), target))


if __name__ == "__main__":
    main()
