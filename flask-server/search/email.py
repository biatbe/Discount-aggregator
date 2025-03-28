from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import csv


# WebDriver Setup
CHROMEDRIVER_PATH = "../chromedriver/chromedriver.exe"

def gather_emails():
    # Set up the WebDriver
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)

    url = "https://www.google.com/maps/d/u/1/viewer?hl=fr&mid=1O88pQS8i5lshCowBfHvhtBG2_v8&ll=50.80801077814669%2C9.93780291565919&z=7"

    try:
        driver.get(url)

        # Wait for page to load
        time.sleep(5)


        tickboxes = driver.find_elements(By.CSS_SELECTOR, ".uVccjd.HzV7m-pbTTYe-PGTmtf")[1:]
        open_arrows = driver.find_elements(By.CSS_SELECTOR, ".uVccjd.HzV7m-pbTTYe-KoToPc-ornU0b-hFsbo.HzV7m-KoToPc-hFsbo-ornU0b")
        results = []

        # for box in tickboxes:
        #     box.click()
        
        # for arrow in open_arrows:
        #     arrow.click()
        open_arrows[0].click()

        # Scroll to bottom
        scroller = driver.find_element(By.CSS_SELECTOR, ".mU4ghb-pbTTYe-n0tgWb-haAclf")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroller)
        time.sleep(2)
        groups = driver.find_elements(By.CSS_SELECTOR, ".HzV7m-pbTTYe-ibnC6b.pbTTYe-ibnC6b-d6wfac")[60:]

        for group in groups:
            group.click()
            dc = {}
            attributes = driver.find_elements(By.CSS_SELECTOR, ".qqvbed-p83tee")
            if group.find_element(By.CSS_SELECTOR, ".suEOdc").text:
                dc["name"] = group.find_element(By.CSS_SELECTOR, ".suEOdc").text
            for attribute in attributes:
                if "Adresse" in attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-V1ur5d").text:
                    dc["address"] = attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-lTBxed").text
                if "PLZ" in attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-V1ur5d").text:
                    dc["postal_code"] = attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-lTBxed").text
                if "Stadt" in attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-V1ur5d").text:
                    dc["city"] = attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-lTBxed").text
                if "E-mail" in attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-V1ur5d").text:
                    dc["email"] = attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-lTBxed").text
                if "Telefon" in attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-V1ur5d").text:
                    dc["phone"] = attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-lTBxed").text
                if "Website" in attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-V1ur5d").text:
                    dc["website"] = attribute.find_element(By.CSS_SELECTOR, ".qqvbed-p83tee-lTBxed").text
            results.append(dc)
            back_arrow = driver.find_elements(By.CSS_SELECTOR, "div.U26fgb.mUbCce.p9Nwte.HzV7m-tJHJj-LgbsSe.qqvbed-a4fUwd-LgbsSe.M9Bg4d")
            if back_arrow and back_arrow[0]:
                back_arrow[0].click()
    
    finally:
        driver.quit()

        csv_filename = "output.csv"

        # Writing to CSV
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = results[0].keys()  # Get headers from the first dictionary
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()  # Write headers
            writer.writerows(results)  # Write multiple rows

        print(f"CSV file '{csv_filename}' created successfully!")
        return results