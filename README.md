# Books Scraper Portfolio

A small Python scraping pipeline that collects data from books.toscrape.com (a practice site built for scraping). It scrapes 1,000 books, cleans the data, tracks price changes over time, and maps each book to its category.

## Features

- **Parallel scraping**: 50 catalogue pages fetched with ThreadPoolExecutor (5 workers)
- **Retry on failure**: each page is retried up to 3 times with increasing wait
- **Data cleaning**: prices converted to numbers, star ratings to integers
- **Price history tracking**: each run logs only books whose price changed
- **Category mapping**: walks every category and its pagination, with a 0.3s delay between requests

## Requirements

Python 3, requests, beautifulsoup4

    pip install requests beautifulsoup4

## How to run

Run the scripts from the same folder, in this order:

    python books_fast.py   # scrape 1000 books -> books_fast.csv
    python clean.py        # clean the data    -> books_clean.csv
    python track.py        # log price changes -> history.csv
    python cats_full.py    # book categories   -> categories.csv

## Files

- books_fast.py: parallel scraper (title, price, rating, stock)
- clean.py: cleans books_fast.csv into books_clean.csv
- track.py: compares prices with history.csv and appends new or changed prices
- cats_full.py: scrapes every category and saves title, category pairs
- books_clean.csv, categories.csv, history.csv: sample output

## Notes

- The first run of track.py saves a baseline; later runs add only changed prices.
- Only public product data is collected. No personal data.
- Built as a portfolio sample for lead-generation and data-scraping work.
