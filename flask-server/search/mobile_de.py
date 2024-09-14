import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def search_vehicle(_type, make, model, maximum_km, body_type, eqLevel, combustion, power_min, power_max, transmission, first_reg=None):
    service = Service(executable_path = "././driver/chromedriver-win64/chromedriver.exe")
    chrome_options = Options()  
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument('--window-size=1920,1080')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')    
    driver = webdriver.Chrome(service= service, options=chrome_options)
    
    driver.get("https://mobile.de")
    driver.implicitly_wait(2)

    driver.find_element(By.XPATH, '//*[text()="Einverstanden"]').click()
    
    # Choosing the type of vehicle
    vehicle_type = driver.find_element(By.CSS_SELECTOR, '[data-testid="qs-segment-tabs"]')
    car = vehicle_type.find_element(By.CSS_SELECTOR, '[data-testid="qs-segment-Car"]')
    motorbike = vehicle_type.find_element(By.CSS_SELECTOR, '[data-testid="qs-segment-Motorbike"]')
    van = vehicle_type.find_element(By.CSS_SELECTOR, '[data-testid="qs-segment-Truck"]')
    if _type == "car":
        car.click()
    elif _type == "van":
        van.click()
    elif _type == "motor":
        motorbike.click()
    else:
        return {"error": "Following type does not exist: " + _type}
    
    
    make_select = driver.find_element(By.CSS_SELECTOR, '[data-testid="qs-select-make"]')
    
    # Select for make
    select = Select(make_select)
    select.select_by_visible_text(make)

    found = False
    
    # Sometimes doesnt find it so we givve it 5 tries
    for _ in range(5):
        model_select = driver.find_element(By.CSS_SELECTOR, '[data-testid="qs-select-model"]')
        option_list_model = model_select.find_elements(By.TAG_NAME, "option")
        option_list_model = map(lambda x: x.text, option_list_model)

        if model in option_list_model:
            found = True
            break
        else:
            time.sleep(0.2)
    
    if not found:
        return {"error": "Model does not exist on following car: " + make}
    else:
        # Select for model
        select = Select(model_select)
        select.select_by_visible_text(model)
    
    first_registration_select = driver.find_element(By.CSS_SELECTOR, '[data-testid="qs-select-1st-registration-from-select"]')
    option_list_reg = first_registration_select.find_elements(By.TAG_NAME, "option")
    option_list_reg = list(map(lambda x: x.text, option_list_reg))
    
    # Select for first registration
    select = Select(first_registration_select)
    
    # Choosing first registration
    # First is "Beliebig"
    if first_reg == None:
        select.select_by_visible_text(option_list_reg[1])
    else:
        if first_reg in option_list_reg:
            select.select_by_visible_text(first_reg)
        else:
            return {"error": "Invalid reg value: " + first_reg}
        
    # Input maximum km data
    max_km = driver.find_element(By.CSS_SELECTOR, '[data-testid="qs-select-mileage-up-to-input"]')
    max_km.send_keys(maximum_km)
    
    # We need more filters so let's go into it
    driver.find_element(By.CSS_SELECTOR, '[data-testid="qs-more-filter"]').click()
    
    # Fill in eqLevel
    # TODO: might need to modify the text, depends if the search matches by regex, ignores dashes etc.
    eqLevel_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="model-description-0"]')
    eqLevel_input.send_keys(eqLevel)
    
    # Vehicle body types (Cabriolet, Hatchback, etc.)
    #suv_label = driver.find_element(By.XPATH, '//label[contains(@data-testid, "categories-filter-OffRoad-checkbox")]')
    cabrio_label = driver.find_element(By.XPATH, '//*[@data-testid="categories-filter-Cabrio-checkbox"]/..')
    hatchback_label = driver.find_element(By.XPATH, '//*[@data-testid="categories-filter-SmallCar-checkbox"]/..')
    limousine_label = driver.find_element(By.XPATH, '//*[@data-testid="categories-filter-Limousine-checkbox"]/..')
    suv_label = driver.find_element(By.XPATH, '//*[@data-testid="categories-filter-OffRoad-checkbox"]/..')
    combi_label = driver.find_element(By.XPATH, '//*[@data-testid="categories-filter-EstateCar-checkbox"]/..')
    coupe_label = driver.find_element(By.XPATH, '//*[@data-testid="categories-filter-SportsCar-checkbox"]/..')
    
    seats = driver.find_element(By.CSS_SELECTOR, '[data-testid="seats-filter-min-input"]')
    
    # Scroll to manual as that is the lowest on the screen
    ActionChains(driver)\
        .scroll_to_element(seats)\
        .perform()
    
    # Selecting the body type based on input
    if body_type == 'cabrio':
        cabrio_label.click()
    elif body_type == 'hatchback':
        hatchback_label.click()
    elif body_type == 'limousine':
        limousine_label.click()
    elif body_type == 'suv':
        suv_label.click()
    elif body_type == 'combi':
        combi_label.click()
    elif body_type == 'coupe':
        coupe_label.click()
    
    
    # Selecting combustion
    petrol_label = driver.find_element(By.XPATH, '//*[@data-testid="fuel-type-filter-PETROL-checkbox"]/..')
    diesel_label = driver.find_element(By.XPATH, '//*[@data-testid="fuel-type-filter-DIESEL-checkbox"]/..')
    electric_label = driver.find_element(By.XPATH, '//*[@data-testid="fuel-type-filter-ELECTRICITY-checkbox"]/..')
    hybrid_diesel_label = driver.find_element(By.XPATH, '//*[@data-testid="fuel-type-filter-HYBRID_DIESEL-checkbox"]/..')
    hybrid_petrol_label = driver.find_element(By.XPATH, '//*[@data-testid="fuel-type-filter-HYBRID-checkbox"]/..')
    plug_in_label = driver.find_element(By.XPATH, '//*[@data-testid="fuel-type-filter-HYBRID_PLUGIN-checkbox"]/..')
    
    # Scroll to plug_in_label as that is the lowest on the screen
    ActionChains(driver)\
        .scroll_to_element(plug_in_label)\
        .perform()
    
    # Selecting combustion based on input
    if combustion == 'petrol':
        petrol_label.click()
    elif combustion == 'diesel':
        diesel_label.click()
    elif combustion == 'electric':
        electric_label.click()
    elif combustion == 'hybrid_diesel':
        hybrid_diesel_label.click()
    elif combustion == 'hybrid_petrol':
        hybrid_petrol_label.click()
    elif combustion == 'plug_in':
        plug_in_label.click()
    
    # Selecting transmission
    manual_label = driver.find_element(By.XPATH, '//*[@data-testid="transmission-filter-MANUAL_GEAR-checkbox"]/..')
    automatic_label = driver.find_element(By.XPATH, '//*[@data-testid="transmission-filter-AUTOMATIC_GEAR-checkbox"]/..')
    
    scroll_to_transmission = driver.find_element(By.CSS_SELECTOR, '[data-testid="fuel-consumption-combined-filter"]')
    
    power_min_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="power-filter-min-input"]')
    power_max_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="power-filter-max-input"]')
    
    # Scroll before clicking
    ActionChains(driver)\
        .scroll_to_element(scroll_to_transmission)\
        .perform()
        
    power_min_input.send_keys(power_min)
    power_max_input.send_keys(power_max)
    
    if transmission == "manual":
        manual_label.click()
    elif transmission == "automatic":
        automatic_label.click()
        
    search_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="stickyBar-submit-search"]')
    search_button.click()
    
    # Sorting by price increasing
    # TODO: Maybe add options next
    wait = WebDriverWait(driver, 10)
    sorting_menu = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="sorting-menu-dropdown"]')))
    select = Select(sorting_menu)
    select.select_by_value("sb=p&od=up")
    
    list_of_cars = driver.find_element(By.CSS_SELECTOR, '[data-testid="result-list-container"]')
    car_divs = list_of_cars.find_elements(By.XPATH, './div')
    car_divs = car_divs[1:]
    filtered_cars = []
    # We don't want to include sponsored cars so we filter them out
    for car in car_divs:
        try:
            car.find_element(By.CSS_SELECTOR, '[data-testid="sponsored-badge"]')
            pass
        except NoSuchElementException:
            filtered_cars.append(car)
            
    prices = []
    for car in filtered_cars:
        try:
            price = car.find_element(By.CSS_SELECTOR, '[data-testid="price-label"]').text
            prices.append(price)
            print(price)
        except NoSuchElementException:
            pass
        
    #prices = list(map(lambda x: x.find_element(By.CSS_SELECTOR, '[data-testid="price-label"]').text, filtered_cars))
    
    # Return some data based on your search logic
    return {"make": prices, "status": "search complete"}