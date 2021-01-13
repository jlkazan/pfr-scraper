import argparse
import sys
from pathlib import Path

from scraping.scraper import Scraper


def parse_args(args) -> argparse.Namespace:
    """
    Function for parsing command line arguments

    :return: The args
    """
    parser = argparse.ArgumentParser(description="Parser for scraping PFF data")

    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=2020,
        help="The year to scrape the data"
        "Default: 2020"
    )

    parser.add_argument(
        "--stat",
        "-s",
        type=str,
        required=True,
        help="The statistic to scrape"
    )

    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        default="output",
        help="The output directory to put the scraped data csv(s)"
        "Default: output"
    )

    return parser.parse_args(args)


def main(args: argparse.Namespace):
    """
    Scrape a pff url and save the data from each table to its own csv in the specified output directory

    :param args: The parsed command line arguments
    """
    url = f"http://www.pro-football-reference.com/years/{args.year}/{args.stat}.htm"
    scraper = Scraper(url=url)
    table_ids = scraper.find_table_ids()

    output_dir_path = Path(args.output_dir)
    if not Path(args.output_dir).exists():
        Path(args.output_dir).mkdir()

    for table_id in table_ids:
        df = scraper.scrape(table_id)
        output_file_path = output_dir_path.joinpath(f"{table_id}.csv")
        print(output_file_path)
        df.to_csv(output_file_path)


if __name__ == '__main__':
    main(parse_args(sys.argv[1:]))
