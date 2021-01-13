# pfr-scraper
Web scraper and plotter (coming soon) for analyzing data on pro-football-reference.com

Currently allows support for scraping basic and advanced player season stats.
Note: Does *not* work for advanced receiving or advanced rushing (currently working on fixing that bug)

Run `python -m scraping.scrape_pff` including command line args for year and stat 
(i.e. receiving, passing_advanced, etc.) in order to scrape pff and get a csv of that table for the season