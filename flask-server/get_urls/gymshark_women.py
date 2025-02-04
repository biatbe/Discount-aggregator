from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver
service = Service("../chromedriver/chromedriver.exe")  # Change this to your driver path
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless if you don't need to see the browser
driver = webdriver.Chrome(service=service, options=options)

url = "https://nl.gymshark.com/collections/outlet/womens"
driver.get(url)

# Wait for page to load
time.sleep(1)

driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()

# Click the "View All" button if it exists
try:
    view_all_button = driver.find_element(By.CLASS_NAME, "pagination_view-all__qrpsC")
    ActionChains(driver).move_to_element(view_all_button).click().perform()
    time.sleep(2)  # Wait for products to load
except:
    print("View All button not found or already clicked.")

# Extract all product links
product_links = [link.get_attribute("href") for link in driver.find_elements(By.CSS_SELECTOR, "div.product-card_image-wrap__J2A_J a")]

# SAVE URLS TO DISK
with open(f'../urls/gymshark_women_urls.txt', 'w') as f:
    f.write('\n'.join(product_links))
    f.close()

# Close the browser
driver.quit()