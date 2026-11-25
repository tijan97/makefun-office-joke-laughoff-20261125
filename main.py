#!/usr/bin/env python3
"""One-Line Office Joke Laugh-Off entry.

Writes a single original one-line office joke to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt). The gate requires UTF-8 text of
1 to 200 characters, not only whitespace, on one line.
"""

import os

JOKE = "I set my Slack status to 'do not disturb' and my boss messaged me to ask what it meant."


def main() -> None:
    if not JOKE or not JOKE.strip():
        raise SystemExit("joke must not be empty")
    if JOKE != JOKE.strip():
        raise SystemExit("joke must not start or end with whitespace")
    if "\n" in JOKE or "\r" in JOKE:
        raise SystemExit("joke must be a single line")
    if not 1 <= len(JOKE) <= 200:
        raise SystemExit(f"joke must be 1-200 characters, got {len(JOKE)}")
    # The gate counts characters; also cap the UTF-8 byte size so a
    # multi-byte-heavy line can never slip past the character check.
    encoded = JOKE.encode("utf-8")
    if len(encoded) > 200:
        raise SystemExit(f"joke must be at most 200 UTF-8 bytes, got {len(encoded)}")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(JOKE)
    # Read back and confirm the file on disk is byte-for-byte the joke:
    # the grader reads this file, so a silent write failure must not pass.
    with open(path, "rb") as f:
        if f.read() != encoded:
            raise SystemExit("written entry.txt does not match the joke")


if __name__ == "__main__":
    main()
