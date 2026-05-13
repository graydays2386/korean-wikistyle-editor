# -*- coding: utf-8 -*-
import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Korean wiki-style editing pipeline."
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-i",
        "--input-file",
        type=Path,
        help="Path to a UTF-8 text file to process.",
    )
    input_group.add_argument(
        "-t",
        "--text",
        type=str,
        help="Raw text to process.",
    )
    input_group.add_argument(
        "--stdin",
        action="store_true",
        help="Read raw text from standard input.",
    )

    parser.add_argument(
        "--output-json",
        type=Path,
        help="Optional path to save the full pipeline result as JSON.",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        help="Optional path to save only the generated Markdown body.",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Input/output file encoding. Default: utf-8.",
    )
    parser.add_argument(
        "--print-body",
        action="store_true",
        help="Print only the generated Markdown body instead of the full result.",
    )

    return parser.parse_args()