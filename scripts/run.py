#!/usr/bin/env python3
"""CLI entry-point for the Superset PO Translator.

Usage::

    python scripts/run.py [INPUT_PO] [OUTPUT_PO]

Defaults to ``messages.po`` → ``messages_it.po`` when no arguments
are provided.
"""

import sys
from pathlib import Path

# Allow running from the project root without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from translator import translate_po_file  # noqa: E402


def main() -> int:
    input_file = sys.argv[1] if len(sys.argv) > 1 else "messages.po"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "messages_it.po"
    translate_po_file(input_file, output_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
