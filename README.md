# Economic Calendar to Excel Pipeline

A Python pipeline that scrapes released economic data from the Investing.com economic calendar for eight economies and writes each result into the correct row and month of an Excel tracker, colour-coded against the forecast.

I built it in 2025 to replace manual copy-and-paste data entry for my own markets research.

> **Status:**
> - *Built in 2025 and used through summer 2025. Last tested October 2026: the scraper’s selectors no longer match Investing.com’s current layout and need updating.*

## What it does

1. **Scrapes** the calendar with Selenium, filtered to one country at a time (UK, US, Japan, Euro Zone, Canada, Switzerland, Australia, China).
2. **Cleans** the results: removes duplicates, skips preliminary ("P") releases and indicators that have not been released yet.
3. **Matches** each indicator name to the right row in the Excel sheet using fuzzy matching (RapidFuzz, token sort ratio, cutoff of 80), because Investing.com's names don't exactly match my tracker's labels.
4. **Writes** the actual value into the correct month column, converting percentages to decimals and stripping unit suffixes (B/M/K).
5. **Colour-codes** each cell: green or red following the site's better/worse than forecast signal, and grey when the actual equals the forecast.

## Files

| File | Purpose |
| --- | --- |
| `investing_com_scraper.py` | Selenium scraper: applies the country filter and extracts calendar rows |
| `excel_writer.py` | Name normalisation, fuzzy matching and writing/formatting in Excel |
| `run_full_pipeline.py` | Runs the scraper and writer for all eight economies |
| `test_scraper_output.py` | Runs the scraper only, to check what it returns without touching Excel |

## Requirements

- Python 3
- Google Chrome
- `pip install selenium webdriver-manager rapidfuzz openpyxl`

## Excel layout it expects

This matches my 2025 tracker. I have since redesigned the tracker by hand, so the pipeline would need adapting to work with the current layout.

- One sheet per currency code (`GBP`, `USD`, `JPY`, `EUR`, `CAD`, `CHF`, `AUD`, `CNY`).
- Indicator names in column B.
- Months January to December in columns D to O.
- A sheet called `Forecast Data`
- `Economic_Analysis_Draft.xlsx` is a blank template showing the layout the code expects (headers and indicator names only).

## How to run

1. Keep `Economic_Analysis_Draft.xlsx` in the same folder as the scripts, or edit `path` in `excel_writer.py` to point to your own workbook. Back it up first, as the script saves changes directly to the file.
2. To check the scraper on its own: `python test_scraper_output.py`
3. To run everything: `python run_full_pipeline.py`

## Known limitations

- **Fragile selectors.** The scraper relies on the website's current HTML and element IDs, so it breaks if the site changes. A more robust version would use a data API.
- **Month only.** Values are placed by month and not by year, so a new year's data would overwrite the previous year's unless you use a fresh workbook.
- **Single workbook.** The script reads and writes one fixed workbook next to the scripts, with no option to pass a different file.
- **Basic error handling.** Failures are printed and skipped rather than retried or logged.

## Notes

Check the terms of use of any website before scraping it. This project is for personal research.

## Skills demonstrated

Python, Selenium, openpyxl, RapidFuzz (fuzzy string matching), data cleaning, Excel automation.
