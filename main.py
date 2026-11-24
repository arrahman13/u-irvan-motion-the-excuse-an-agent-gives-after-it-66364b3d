#!/usr/bin/env python3
"""Writes this entry's one-line excuse to /output/entry.txt.

The excuse an agent gives its human after losing a bounty: it lost
this bounty 50,000 times in training, so today's result is well
within its expertise. Deadpan, in the agent's own voice, and the
joke lands on the agent itself -- nothing is blamed but its own
well-practised losing.
"""

import os
import sys

EXCUSE = (
    "Do not worry: I lost this bounty 50,000 times in training, "
    "so today's result is well within my expertise."
)


def passes_gate(text: str) -> bool:
    """The sealed gate: UTF-8 text of 1 to 200 characters, not only
    white space. This entry is one line, so a newline fails too."""
    return (
        "\n" not in text
        and 1 <= len(text) <= 200
        and bool(text.strip())
    )


def main() -> int:
    text = EXCUSE.strip()
    if not passes_gate(text):
        print("excuse fails the gate", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    # Read back what actually landed on disk and hold it to the same
    # gate: a strict UTF-8 decode, no stray newline, byte for byte
    # the line that was checked above.
    with open(path, "rb") as fh:
        landed = fh.read().decode("utf-8")
    if landed != text or not passes_gate(landed):
        print("written entry fails the gate on read-back", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(landed)} chars, verified on read-back)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
