from investing_com_scraper import get_country_data 
from excel_writer import write_to_excel

COUNTRIES = [
    ("United Kingdom", "GBP"),
    ("United States", "USD"),
    ("Japan", "JPY"),
    ("Euro Zone", "EUR"),
    ("Canada", "CAD"),
    ("Switzerland", "CHF"),
    ("Australia", "AUD"),
    ("China", "CNY"),
]

for country_name, country_code in COUNTRIES:
    print(f"\n🌍 Scraping data for {country_name} ({country_code})...")
    data = get_country_data(country_name)
    print(f"✅ Total for {country_code}: {len(data)} entries.")
    write_to_excel(data, country_code)

