# -*- coding: utf-8 -*-
from app.cli.args import parse_args
from app.cli.io import load_input, save_outputs, print_result
from app.util.agents_new.pipeline import run_pipeline

def main() -> None:
    args = parse_args()
    raw_text = load_input(args)

    if not raw_text:
        raise ValueError("Input text is empty.")

    result = run_pipeline(raw_text)

    save_outputs(result, args)
    print_result(result, print_body=args.print_body)

if __name__ == "__main__":
    main()