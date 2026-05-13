# -*- coding: utf-8 -*-
import argparse
import json
import sys


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


def print_result(result: dict, print_body: bool = False) -> None:
    print("\n--- 파이프라인 최종 결과 ---")

    if print_body:
        print(result.get("body", ""))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))