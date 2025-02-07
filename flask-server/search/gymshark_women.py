from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# WebDriver Setup
CHROMEDRIVER_PATH = "../chromedriver/chromedriver.exe"

# Read URLs
with open("../urls/gymshark_women_urls.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]

def getPrice(price):
    number = ''
    for c in price:
        if c.isdigit():
            number += c
        if c == '.' or c == ',':
            number += '.'
    return float(number)

def scrape_product(url, counter):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 2)

        # Click accept cookies if available
        cookie_button = driver.find_elements(By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
        if cookie_button:
            cookie_button[0].click()

        stripped_product = {
            "id": counter,
            "brand": "gymshark",
            "sectionName": "women",
            "href": url
        }

        # Get Product Name
        name_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-information_title__3jR8K")))
        stripped_product["name"] = name_element.text

        # Get Prices
        price_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-information_price__pEWjj")))
        price_elements = price_container.find_elements(By.TAG_NAME, "div")

        if len(price_elements) < 2:
            return None
        stripped_product["price"] = getPrice(price_elements[0].text.strip())
        stripped_product["oldPrice"] = getPrice(price_elements[1].text.strip())
        stripped_product["displayDiscountPercentage"] = int(((stripped_product["oldPrice"] - stripped_product["price"]) / stripped_product["oldPrice"]) * 100)

        # Get Image URL
        image_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.image-gallery_gallery--item__OW3UF img")))
        stripped_product["url"] = image_element.get_attribute("src")

    finally:
        driver.quit()

    return stripped_product

def gather_items():
    product_names = []
    
    # Use ThreadPoolExecutor to speed up processing
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust `max_workers` based on your system
        future_to_url = {executor.submit(scrape_product, url, i+1): url for i, url in enumerate(urls)}

        for future in as_completed(future_to_url):
            try:
                product = future.result()
                if product is not None:
                    print(product)  # Print each product as it's processed
                    product_names.append(product)
            except Exception as e:
                print(f"Error processing {future_to_url[future]}: {e}")

    return product_names

# Run the scraper
products = gather_items()
