import argparse
import tqdm
import re
import os
from itertools import islice

parser = argparse.ArgumentParser(description="")

parser.add_argument("--input_dir", type=str)
parser.add_argument("--output_dir", type=str)

MINIMUM_LINES = 5
BRACKET_REGEX = r"\{(.*?)\};"


def newline_filter(fn: str) -> bool:
    with open(fn, "rt") as fn_reader:
        return len(list(islice(fn_reader, 0, MINIMUM_LINES))) == MINIMUM_LINES


def bracket_content_removal(output_dir: str, fn: str) -> None:
    base_fn = os.path.basename(fn)
    out_fn = os.path.join(output_dir, base_fn)
    with open(fn, "rt") as fn_reader, open(out_fn, "wt") as fn_writer:
        raw_file = fn_reader.read()
        # might need flags for re.M according to https://stackoverflow.com/a/35688301
        brackets_removed = re.sub(BRACKET_REGEX, " ", raw_file)
        fn_writer.write(brackets_removed)


def process_and_filter(input_dir: str, output_dir: str) -> None:
    def full_path(f):
        return os.path.join(input_dir, f)

    relevant_files = filter(newline_filter, map(full_path, os.listdir(input_dir)))
    for fn in tqdm.tqdm(relevant_files, desc="Processing Files"):
        bracket_content_removal(output_dir, fn)


def main():
    args = parser.parse_args()
    process_and_filter(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
