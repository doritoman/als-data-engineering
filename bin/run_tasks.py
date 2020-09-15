#!/usr/bin/python3
import argparse

from etl import get_acquisition_facts, get_people


def run_tasks(input_path, output_path):
    print("Running task 1...\n----------")
    get_acquisition_facts(input_path, output_path)
    print("Running task 2...\n----------")
    get_people(input_path, output_path)


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(
        prog="run_tasks",
        description="Runs all tasks for ALS Data Engineering.",
    )
    args_parser.add_argument(
        "-i",
        "--input-path",
        type=str,
        default="static/input",
        help="The path containing containing the CSV input files.",
    )
    args_parser.add_argument(
        "-o",
        "--output-path",
        type=str,
        default="static/output",
        help="The path where the output CSV files will be stored.",
    )
    args = args_parser.parse_args()
    run_tasks(args.input_path, args.output_path)
