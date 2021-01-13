from typing import List

from bs4 import BeautifulSoup, Comment
import pandas as pd
from urllib.request import urlopen


class Scraper:
    """
    General class for scraping data from pro-football-reference.com

    Methods were inspired by the following source:
            https://towardsdatascience.com/scraping-nfl-stats-to-compare-quarterback-efficiencies-4989642e02fe
            https://github.com/BenKite/football_data/blob/master/profootballReferenceScrape.py
    """
    def __init__(self, url: str):
        self.url = url

    def find_table_ids(self) -> List[str]:
        """
        Function for scraping the url in order to determine the table ids for each table in the url
        :return: A list of the table ids
        """
        # Open URL and pass the html to BeautifulSoup
        html = urlopen(self.url)
        stats_page = BeautifulSoup(html, features="html.parser")

        # Remove all comments from the html
        # Code from: https://stackoverflow.com/questions/23299557/beautifulsoup-4-remove-comment-tag-and-its-content
        for element in stats_page(text=lambda text: isinstance(text, Comment)):
            element.extract()

        # Get all of the divs that may have a table
        divs = stats_page.findAll('div', id="content")
        divs = divs[0].findAll("div", attrs={"class": "table_container"})

        # Iterate through each div looking for tables
        table_ids = []
        for div in divs:
            table_str = str(div.findAll("table"))
            table_id = table_str[table_str.find("id=") + 3: table_str.find(">")]
            # Remove " characters
            table_id = table_id.replace("\"", "")
            if len(table_id) > 0:
                table_ids.append(table_id)
        return table_ids

    def scrape(self, table_id: str) -> pd.DataFrame:
        """
        Function for scraping the url and turning the data into a pandas DataFrame

        :param table_id: A string representing the table id, which can be found with the find_table_ids method
        :return: A DataFrame consisting of the scraped table data from pfr
        """
        # Open URL and pass the html to BeautifulSoup
        html = urlopen(self.url)
        stats_page = BeautifulSoup(html, features="html.parser")
        tables = stats_page.findAll("table", id=table_id)

        # Obtain table headers
        table_header = tables[0].findAll("thead")
        over_header = table_header[0].findAll("tr", attrs={"class": "over_header"})
        column_headers = table_header[0].findAll("tr")[0] if len(over_header) == 0 else table_header[0].findAll("tr")[1]
        column_headers = [i.getText() for i in column_headers.findAll("th")]

        # Obtain table rows
        table_body = tables[0].findAll("tbody")
        table_rows = table_body[0].findAll("tr")

        # Aggregate data from each row into an array
        rows_data = []
        for row in table_rows:
            row_data = [col.getText() for col in row.findAll("td")]
            rows_data.append(row_data)

        # Create DataFrame from the array of scraped data
        data = pd.DataFrame(rows_data, columns=column_headers[1:])

        return data
