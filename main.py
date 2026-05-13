# -*- coding: utf-8 -*-
import argparse
import json
import sys
from pathlib import Path

from app.util.agents_new.pipeline import run_pipeline


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


def load_input(args: argparse.Namespace) -> str:
    if args.input_file:
        if not args.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {args.input_file}")
        return args.input_file.read_text(encoding=args.encoding).strip()

    if args.text:
        return args.text.strip()

    if args.stdin:
        return sys.stdin.read().strip()

    raise ValueError("No input source provided.")


def save_outputs(result: dict, args: argparse.Namespace) -> None:
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding=args.encoding,
        )

    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        body = result.get("body", "")
        args.output_md.write_text(body, encoding=args.encoding)


def main() -> None:
    args = parse_args()
    raw_text = load_input(args)

    if not raw_text:
        raise ValueError("Input text is empty.")

    result = run_pipeline(raw_text)

    save_outputs(result, args)

    print("\n--- 파이프라인 최종 결과 ---")
    if args.print_body:
        print(result.get("body", ""))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()