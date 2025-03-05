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

def get_promotion_link():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--window-size=400,1080")
    #service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(options=options)
    
    try:
        url = "https://shop.mango.com/nl"
        driver.get(url)

        time.sleep(2)
        # Click accept cookies if available
        cookie_button = driver.find_element(By.ID, "cookies.button.acceptAll")
        if cookie_button:
            cookie_button.click()

        time.sleep(1)
        hamburger_button = driver.find_element(By.CSS_SELECTOR, "div .WrapperMenu_menu__nrL6m")
        hamburger_button.click()
        time.sleep(1)
        top_div = driver.find_element(By.CSS_SELECTOR, "div .TopBar_topBar__VrJV_")
        gentlemen = top_div.find_elements(By.CSS_SELECTOR, ".BrandEntry_brandLi__AAzaN")
        gentlemen[1].click()
        time.sleep(1)
        bottom_div = driver.find_element(By.CSS_SELECTOR, "div .StructureSM_content__P2E86")
        promotion = bottom_div.find_elements(By.CSS_SELECTOR, ".Columns_column__JWxmA li")
        promotion[5].click()
        time.sleep(1)
        container = driver.find_element(By.CSS_SELECTOR, "div .InteriorMenu_open__mtTEg")
        type_links = container.find_elements(By.CSS_SELECTOR, ".Columns_column__JWxmA li")
        view_all = type_links[0].find_element(By.CSS_SELECTOR, "a")
        promotion_url = view_all.get_attribute("href")

        return promotion_url
    finally:
        driver.quit()

def gather_items():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--window-size=1920,1080")
    #service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(options=options)
    
    try:
        url = get_promotion_link()
        driver.get(url)
        wait = WebDriverWait(driver, 2)

        time.sleep(2)
        # Click accept cookies if available
        cookie_button = driver.find_element(By.ID, "cookies.button.acceptAll")
        if cookie_button:
            cookie_button.click()

        # Wait for new content to load
        time.sleep(2)

        print("Started scrolling!")
        while True:
            
            # Scroll down to the bottom
            driver.execute_script("window.scrollBy(0, 2000);")
            
            # Wait for new content to load
            time.sleep(0.2)
            
            # Calculate new scroll height and compare with the last height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height - driver.execute_script("return window.scrollY") < 1500:  
                break

        print("Finished scrolling!")
        
        # Get all products
        ul_element = driver.find_element(By.CLASS_NAME, "Grid_grid__fLhp5.Grid_standard__xt7_3")
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")

        products = []

        print("Started getting products!")
        for i, li in enumerate(li_elements):
            product_name = li.find_elements(By.CLASS_NAME, "ProductTitle_productTitle___cM9O")
            # There is a possibility that there are empty cards in which case we just continue
            if not product_name:
                continue
            product_name = product_name[0].text.strip()
            prev_price = getPrice(li.find_element(By.CSS_SELECTOR, ".SinglePrice_crossed__BjBEu.SinglePrice_center__mfcM3.texts_bodyM__lR_K7.texts_bodyM__lR_K7").text)
            new_price = getPrice(li.find_element(By.CSS_SELECTOR, ".SinglePrice_center__mfcM3.texts_bodyM__lR_K7.SinglePrice_finalPrice__CGsuZ").text)
            link_element = li.find_elements(By.CSS_SELECTOR, "div.ProductImage_productImage__cS5d9.ProductImage_fadeIn__iWh0L a")
            link = None
            if link_element:
                link = link_element[0].get_attribute("href")
            image_element = li.find_elements(By.CSS_SELECTOR, ".ProductImage_imageWrapper__dcoT9 img")
            image = None
            if image_element:
                image = image_element[0].get_attribute("srcset").split()[0]

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

        print("Finished getting products!")

    finally:
        driver.quit()

    print(len(li_elements), len(products))
    return products
                