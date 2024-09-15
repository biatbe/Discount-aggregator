
import { NextResponse } from 'next/server';
import puppeteer, { Locator } from 'puppeteer';

const url = "https://mobile.de";

export async function POST(req: Request) {
    const {_type, make, model, maximum_km, body_type, eqLevel, combustion, power_min, power_max, transmission, first_reg} :
        {_type:string, make:string, model:string, maximum_km:number, body_type:string, eqLevel:string,
             combustion:string, power_min:number, power_max:number, transmission:string, first_reg:number}
     = await req.json();

    try {
        // Launch puppeteer
        const browser = await puppeteer.launch({
            headless: false,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--ignore-certificate-errors',
            ]
        });
        const page = await browser.newPage();
        page.setViewport({
            height: 1280,
            width: 960
        })

        // Important when run in headless mode as some sites disable auto search
        // Some sites might still be able to block headless
        const ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36";
        await page.setUserAgent(ua);
        
        // Navigate to the login page
        await page.goto(url);

        page.locator('button')
            .filter(button => button.innerText === 'Einverstanden')
            .click();
    
        // Choosing the type of vehicle
        await page.evaluate((_type) => {
            const vehicle_type = document.querySelector('div[data-testid="qs-segment-tabs"]')
            const car = vehicle_type!.querySelector('div[data-testid="qs-segment-Car"]')
            const motorbike = vehicle_type!.querySelector('div[data-testid="qs-segment-Motorbike"]')
            const van = vehicle_type!.querySelector('div[data-testid="qs-segment-Truck"]')
            if (_type == "car") {
                (car as HTMLElement).click()
            }
            else if (_type == "van") {
                (van as HTMLElement).click()
            }
            else if (_type == "motor") {
                (motorbike as HTMLElement).click()
            }
            else {
                return NextResponse.json({status: 400, message: "Following type does not exist: ", _type})
            }
        }, _type);

        
        // Select for make
        const make_value = await page.evaluate((make) => {
            const make_select = document.querySelector('select[data-testid="qs-select-make"]')
            const select = Array.from(make_select!.querySelectorAll('option'));
            const selected_option = select!.find((element : any) => element.textContent.toLowerCase() == make.toLowerCase())
            if (selected_option) {
                return selected_option.getAttribute('value')
            } else {
                return null;
            }
        }, make);

        if (make_value == null) {
            return NextResponse.json({status: 400, message: "Cannot find following make: ", make})
        } else {
            await page.locator('select[data-testid="qs-select-make"]').fill(make_value) 
        }

        await page.waitForSelector('select[data-testid="qs-select-model"]:not([disabled])')

        // Select for model
        const model_value = await page.evaluate((model) => {
            const model_select = document.querySelector('select[data-testid="qs-select-model"]')
            const select = Array.from(model_select!.querySelectorAll('option'));
            const selected_option = select!.find((element : any) => element.textContent.toLowerCase() == model.toLowerCase())
            if (selected_option) {
                return selected_option.getAttribute('value')
            } else {
                return null;
            }
        }, model);

        if (model_value == null) {
            return NextResponse.json({status: 400, message: "Cannot find following model: ", model})
        } else {
            await page.locator('select[data-testid="qs-select-model"]').fill(model_value) 
        }


        
        const first_registration_select = page.locator('[data-testid="qs-select-1st-registration-from-select"]')
        first_registration_select.fill(String(first_reg))
            
        // Input maximum km data
        const max_km = page.locator('[data-testid="qs-select-mileage-up-to-input"]')
        max_km.fill(String(maximum_km))
        
        // We need more filters so let's go into it
        page.locator('[data-testid="qs-more-filter"]').click()
        
        // Fill in eqLevel
        // TODO: might need to modify the text, depends if the search matches by regex, ignores dashes etc.
        await new Promise(resolve => setTimeout(resolve, 1500));
        const eqLevel_input = page.locator('[data-testid="model-description-0"]')
        eqLevel_input.fill(eqLevel)

        await new Promise(resolve => setTimeout(resolve, 500));
        // Vehicle body types (Cabriolet, Hatchback, etc.)
        const cabrio_label = page.locator('xpath=//input[@data-testid="categories-filter-Cabrio-checkbox"]/..')
        const hatchback_label = page.locator('xpath=//input[@data-testid="categories-filter-SmallCar-checkbox"]/..')
        const limousine_label = page.locator('xpath=//input[@data-testid="categories-filter-Limousine-checkbox"]/..')
        const suv_label = page.locator('xpath=//input[@data-testid="categories-filter-OffRoad-checkbox"]/..')
        const combi_label = page.locator('xpath=//input[@data-testid="categories-filter-EstateCar-checkbox"]/..')
        const coupe_label = page.locator('xpath=//input[@data-testid="categories-filter-SportsCar-checkbox"]/..')
        
        // Selecting the body type based on input
        switch (body_type) {
            case "cabrio":
                cabrio_label.click()
                break;
            case "hatchback":
                hatchback_label.click()
                break;
            case "limousine":
                limousine_label.click()
                break;
            case "suv":
                suv_label.click()
                break;
            case "combi":
                combi_label.click()
                break;
            case "coupe":
                coupe_label.click()
                break;
            default:
                console.log("Unknown body type")
                break;
        }
        
        await new Promise(resolve => setTimeout(resolve, 500));

        // Selecting combustion
        const petrol_label = page.locator('xpath=//input[@data-testid="fuel-type-filter-PETROL-checkbox"]/..')
        const diesel_label = page.locator('xpath=//input[@data-testid="fuel-type-filter-DIESEL-checkbox"]/..')
        const electric_label = page.locator('xpath=//input[@data-testid="fuel-type-filter-ELECTRICITY-checkbox"]/..')
        const hybrid_diesel_label = page.locator('xpath=//input[@data-testid="fuel-type-filter-HYBRID_DIESEL-checkbox"]/..')
        const hybrid_petrol_label = page.locator('xpath=//input[@data-testid="fuel-type-filter-HYBRID-checkbox"]/..')
        const plug_in_label = page.locator('xpath=//input[@data-testid="fuel-type-filter-HYBRID_PLUGIN-checkbox"]/..')

        const scrollAndClick = async (locator : Locator<Element>) => {
            await locator.click();
        }
        
        // Selecting combustion based on input
        switch (combustion) {
            case 'petrol':
                await scrollAndClick(petrol_label)
                break
            case 'diesel':
                await scrollAndClick(diesel_label)
                break
            case 'electric':
                await scrollAndClick(electric_label)
                break
            case 'hybrid_diesel':
                await scrollAndClick(hybrid_diesel_label)
                break
            case 'hybrid_petrol':
                await scrollAndClick(hybrid_petrol_label)
                break
            case 'plug_in':
                await scrollAndClick(plug_in_label)
                break
            default:
                console.log("Couldn't find following combustion type: ", combustion)
                break
        }

        await new Promise(resolve => setTimeout(resolve, 500));
        
        page.locator('[data-testid="power-filter-min-input"]').fill(String(power_min))
        await new Promise(resolve => setTimeout(resolve, 500));
        page.locator('[data-testid="power-filter-max-input"]').fill(String(power_max))
        await new Promise(resolve => setTimeout(resolve, 500));
        await page.evaluate(() => {
            window.scrollTo(0, document.body.scrollHeight);
        });
        await new Promise(resolve => setTimeout(resolve, 500));

        // Selecting transmission
        const manual_label = page.locator('xpath=//input[@data-testid="transmission-filter-MANUAL_GEAR-checkbox"]/..')
        const automatic_label = page.locator('xpath=//input[@data-testid="transmission-filter-AUTOMATIC_GEAR-checkbox"]/..')
        
        if (transmission == "manual") {
            manual_label.click()
        }
        else if (transmission == "automatic") {
            automatic_label.click()
        }

        await new Promise(resolve => setTimeout(resolve, 500));
        
        const search_button_sticky = page.locator('[data-testid="stickyBar-submit-search"]')
        const search_button_above = page.locator('[data-testid="aboveFilter-submit-search"]')
        if (search_button_sticky) {
            search_button_sticky.click()
        } else {
            search_button_above.click()
        }
        
        // Sorting by price increasing
        // TODO: Maybe add options next
        await page.waitForSelector('[data-testid="sorting-menu-dropdown"]')
        const sort_value = await page.evaluate(() => {
            const sort_select = document.querySelector('select[data-testid="sorting-menu-dropdown"]')
            const select = Array.from(sort_select!.querySelectorAll('option'));
            const selected_option = select!.find((element : any) => element.textContent.toLowerCase() == "Preis (niedrigster zuerst)".toLowerCase())
            if (selected_option) {
                return selected_option.getAttribute('value')
            } else {
                return null;
            }
        });

        if (sort_value == null) {
            return NextResponse.json({status: 400, message: "Cannot find sorting!"})
        } else {
            await page.locator('select[data-testid="sorting-menu-dropdown"]').fill(sort_value) 
        }
        
        await page.waitForSelector('[data-testid="result-list-container"]')
        const filtered_cars = await page.evaluate(() => {
            const list_of_cars = document.querySelector('[data-testid="result-list-container"]')
            console.log(list_of_cars)
            if (!list_of_cars) return [];
            const car_divs = Array.from(list_of_cars.children)
            car_divs.shift()
            const filtered_cars : any[] = [];
            console.log(car_divs)
            for (const car of car_divs) {
                try {
                    const sponsored = car.querySelector('[data-testid="sponsored-badge"]');
                    if (!sponsored) {
                        // If no sponsored badge, add the car to filtered cars
                        filtered_cars.push(car);
                    }
                }
                catch (error) {
                    console.error('Error while processing car div:', error);
                }
            }
            return filtered_cars
        });


        console.log(filtered_cars)
                
        // prices = []
        // for car in filtered_cars:
        //     try:
        //         price = car.find_element(By.CSS_SELECTOR, '[data-testid="price-label"]').text
        //         prices.append(price)
        //         print(price)
        //     except NoSuchElementException:
        //         pass
            
        // #prices = list(map(lambda x: x.find_element(By.CSS_SELECTOR, '[data-testid="price-label"]').text, filtered_cars))
        
        // # Return some data based on your search logic

        return NextResponse.json({status: 200, message: "Success"})

    } catch (error) {   
        console.error(`Error while searching for ${make}:`, error);
        return NextResponse.json({status: 400, message: error});
    }

}