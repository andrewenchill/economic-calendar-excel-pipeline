from investing_com_scraper import get_country_data

tracked_economies = {
    "GBP": "United Kingdom",
    "USD": "United States",
    "JPY": "Japan",
    "EUR": "Euro Zone",
    "CAD": "Canada",
    "CHF": "Switzerland",
    "AUD": "Australia",
    "CNY": "China"
}

all_data = {}

for code, country in tracked_economies.items():
    print(f"\n🌍 Scraping data for {country} ({code})...")
    country_data = get_country_data(country)
    all_data[code] = country_data
    print(f"✅ Total for {code}: {len(country_data)} entries.")
