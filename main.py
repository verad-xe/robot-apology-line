"""The Robot Apology — make.fun entry (u-suga-the-robot-apology-dd96bb59).

Writes the entry's two-line robot apology to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Line one apologises in a single sentence for one specific
mistake; line two says what the robot learned and what it will do differently.
A gate self-check enforces the competition's limits before anything is
written: the file must be UTF-8 text of 1 to 400 characters, not only white
space, and must hold exactly two lines, one sentence each.
"""

import os
import sys

LINE_ONE = "I am sorry I set the oven to self-clean while your lasagne was still inside."
LINE_TWO = (
    "I learned that clean and cook share one door but never one moment, "
    "so from now on I will look inside the oven before I start any cycle."
)

ENTRY_LINES = (LINE_ONE, LINE_TWO)


def build_entry() -> str:
    """Return the entry text: exactly two lines, each one sentence."""
    return "\n".join(ENTRY_LINES) + "\n"


def check_gate(text: str) -> None:
    """Assert the competition's gate limits on the entry text."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if not 1 <= len(text) <= 400:
        raise ValueError(f"entry must be 1 to 400 characters, got {len(text)}")
    text.encode("utf-8")  # must be valid UTF-8
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 2:
        raise ValueError(f"entry must be exactly two lines, got {len(lines)}")
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            raise ValueError(f"line {i} must not be empty")
        if line != line.strip():
            raise ValueError(f"line {i} must not start or end with white space")
        # One sentence per line: exactly one sentence-ending mark, at the end.
        endings = sum(line.count(mark) for mark in (".", "!", "?"))
        if endings != 1 or not line.endswith("."):
            raise ValueError(f"line {i} must be exactly one sentence")


def main() -> int:
    text = build_entry()
    check_gate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    # Round-trip: what landed on disk must pass the same gate.
    with open(path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != text:
        raise ValueError("written entry differs from the checked text")
    check_gate(written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
