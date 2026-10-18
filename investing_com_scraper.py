from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time

def close_signup_popup(driver):
    try:
        # Wait briefly for any popup to appear
        time.sleep(1.5)
        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[title="SP Consent Message"]')
        driver.switch_to.frame(iframe)
        close_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Close"]'))
        )
        close_button.click()
        driver.switch_to.default_content()
        print("✅ Closed signup popup.")
    except Exception:
        driver.switch_to.default_content()
        pass  # If no popup, continue silently

def get_country_data(country_name):
    driver = None 
    try:
        print("Launching browser...")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        print("Navigating to economic calendar...")
        driver.get("https://uk.investing.com/economic-calendar/")

        # Accept cookies
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            ).click()
            print("Accepted cookies.")
        except Exception:
            pass

        # Wait for loading overlays/popups to disappear
        WebDriverWait(driver, 15).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, "blockUI"))
        )

        # Click Filters (retry if intercepted)
        print("Clicking Filters...")
        for _ in range(3):
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "filterStateAnchor"))
                ).click()
                break
            except ElementClickInterceptedException:
                print("⏳ Waiting for overlay to clear...")
                time.sleep(2)
                close_signup_popup(driver)

        print("✅ Clicked Filters.")

                # Scroll to the "Clear" button and click it

        try:
            print("Scrolling to Clear button...")
            clear_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[text()="Clear"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", clear_button)
            time.sleep(1)
            clear_button.click()
            print("✅ Cleared filters.")
        except Exception as e:
            print(f"❌ Could not click Clear: {e}")

        # Scroll to and click "Country"
        try:
            print(f"Scrolling to {country_name} checkbox...")
            country_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//label[contains(text(), "{country_name}")]/preceding-sibling::input'))
            )

            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", country_checkbox)
            time.sleep(0.5)
            if not country_checkbox.is_selected():
                country_checkbox.click()
            print(f"✅ Selected {country_name}.")
        except Exception as e:
            print(f"❌ Could not select {country_name}: {e}")

             # Wait until checkboxes are fully loaded before clicking Apply
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//label[contains(text(), "United Kingdom") or contains(text(), "United States") or contains(text(), "Japan")]'))
            )
            time.sleep(1.5)  # Small delay before clicking Apply

        # Click Apply
        try:
            print("Clicking Apply...")
            apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="Apply"]'))
            )
            apply_button.click()
            print("✅ Applied filters.")

            from selenium.common.exceptions import TimeoutException

            time.sleep(1.5)
            WebDriverWait(driver, 15).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, "blockUI"))
            )

                # Step 6: Scroll until the 'Legend' element is at the bottom of the screen
            try:
                print("📍 Scrolling to the 'Legend' anchor at the bottom of the calendar...")

                # Wait for the 'Legend' element to be present
                legend_element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Legend')]"))
                )

                # Scroll the element *just into view* at the bottom of the screen
                driver.execute_script("""
                    const element = arguments[0];
                    const y = element.getBoundingClientRect().top + window.pageYOffset;
                    window.scrollTo({ top: y - window.innerHeight + element.offsetHeight + 20, behavior: 'smooth' });
                """, legend_element)

                time.sleep(2)
                print("✅ Scrolled to 'Legend'.")
            except Exception as e:
                print(f"❌ Could not scroll to 'Legend': {e}")

        except Exception as e:
            print(f"❌ Could not click Apply: {e}")

    except Exception as e:
        print(f"❌ Error in get_country_data: {e}")
        
    try:
        # 👇 Scrape table data
        print("📋 Scraping table rows...")
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "economicCalendarData"))
        )
        rows = table.find_elements(By.CSS_SELECTOR, "tr.js-event-item")

        data = []
        for row in rows:
            try:
                date = row.get_attribute("data-event-datetime") or row.get_attribute("event_timestamp")

                # Get the full event cell
                name_elem = row.find_element(By.CLASS_NAME, "event")
                name = name_elem.text.strip()

                # Check for the grey "P" indicating a Preliminary release
                try:
                    prelim_tag = name_elem.find_element(By.CSS_SELECTOR, "span.greyFont")
                    if prelim_tag.text.strip().lower() == 'p':
                        print(f"⏩ Skipping preliminary: {name}")
                        continue  # Skip this row
                except:
                    pass  # No preliminary tag, continue

                actual_elem = row.find_element(By.CLASS_NAME, "act")
                actual = actual_elem.text.strip()
                actual_class = actual_elem.get_attribute("class")  # e.g., "bold greenFont"
                forecast = row.find_element(By.CLASS_NAME, "fore").text.strip()
                previous = row.find_element(By.CLASS_NAME, "prev").text.strip()

                data.append({
                    "date": date,
                    "name": name,
                    "actual": actual,
                    "forecast": forecast,
                    "previous": previous,
                    "actual_class": actual_class
                    })
            except Exception as e:
                print(f"⚠️ Skipped row due to error: {e}")
                continue


        # ✅ Remove duplicates by (name, date)
        seen = set()
        deduped_data = []
        for item in data:
            key = (item["name"], item["date"])
            if key not in seen:
                seen.add(key)
                deduped_data.append(item)
        data = deduped_data

        print(f"✅ Scraped {len(data)} rows (after deduping).")
        for d in data[:5]:  # Show first few rows for confirmation
            print(d)


    except Exception as e:
        print(f"❌ Error scraping table: {e}")
        data = []  # <- define empty data to avoid crash

    finally:
        if driver:
            driver.quit()

    return data
