import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# WebDriver Setup
CHROMEDRIVER_PATH = "../chromedriver/chromedriver.exe"

def getPrice(price):
    number = ''
    for c in price:
        if c.isdigit():
            number += c
        if c == '.' or c == ',':
            number += '.'
    return float(number)

def gather_items():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        url = "https://shop.mango.com/nl/nl/c/heren/sale--70_3b6679e9"
        driver.get(url)
        wait = WebDriverWait(driver, 2)

        # Click accept cookies if available
        # cookie_button = driver.find_elements(By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
        # if cookie_button:
        #     cookie_button[0].click()

        # Scroll until no more new content is loaded
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            time.sleep(1)
            
            # Calculate new scroll height and compare with the last height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Get all products
        ul_element = driver.find_element(By.CLASS_NAME, "Grid_grid__fLhp5.Grid_standard__xt7_3")
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")

        products = []

        for i, li in enumerate(li_elements):
            product_name = li.find_element(By.CLASS_NAME, "ProductTitle_productTitle___cM9O").text.strip()
            prev_price = getPrice(li.find_element(By.CLASS_NAME, "SinglePrice_crossed__BjBEu SinglePrice_center__mfcM3 texts_bodyM__lR_K7 texts_bodyM__lR_K7").text)
            new_price = getPrice(li.find_element(By.CLASS_NAME, "SinglePrice_center__mfcM3 texts_bodyM__lR_K7 SinglePrice_finalPrice__CGsuZ").text)
            link = li.find_element(By.CSS_SELECTOR, "div.ProductImage_productImage__cS5d9 ProductImage_fadeIn__iWh0L a").get_attribute("href")
            image = li.find_element(By.CLASS_NAME, "ProductImage_imageWrapper__dcoT9").get_attribute("srcset")

            stripped_product = {
                "id": i + 1,
                "brand": "mango",
                "sectionName": "men",
                "href": link,
                "name": product_name,
                "price": new_price,
                "oldPrice": prev_price,
                "displayDiscountPercentage": int(((prev_price - new_price) / prev_price) * 100),
                "url": image
            }

            products.append(stripped_product)

    finally:
        driver.quit()

    return products
                