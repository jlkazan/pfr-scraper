import argparse
import sys
from pathlib import Path
import pandas as pd

from plotting.plotter import Plotter


def parse_args(args) -> argparse.Namespace:
    """
    Function for parsing command line arguments

    :return: The args
    """
    parser = argparse.ArgumentParser(description="Parser for scraping PFF data")

    parser.add_argument(
        "--col1_name",
        "-c1",
        type=str,
        required=True,
        help="The name of the first column to plot"
    )

    parser.add_argument(
        "--col2_name",
        "-c2",
        type=str,
        required=True,
        help="The name of the second column to plot"
    )

    parser.add_argument(
        "--input_csv",
        "-i",
        type=str,
        required=True,
        help="The input csv to plot"
    )

    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=50,
        help="The max number of rows of the csv to plot"
             "Default: 50"
    )

    return parser.parse_args(args)


def main(args: argparse.Namespace):
    """
    Plot the given two columns of the csv at the given path

    :param args: The parsed command line arguments
    """

    input_csv_path = Path(args.input_csv)
    # Assert input csv path exists
    assert input_csv_path.exists(), f"Input csv path does not exist"
    csv_df = pd.read_csv(input_csv_path)

    plotter = Plotter(csv_df)
    plotter.plot(args.col1_name, args.col2_name, args.limit)


if __name__ == '__main__':
    main(parse_args(sys.argv[1:]))
