import requests

def gather_items():
    headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"}

    resp = requests.get("https://www.zara.com/nl/en/categories?categoryId=0&categorySeoId=7139&ajax=true", headers=headers)
    data = resp.json()
    categories = data["categories"]
    categoryId = 0
    for category in categories:
        if category["name"] == "MAN":
            for subcategory in category["subcategories"]:
                if subcategory["name"] == "SALE":
                    for subsubcategory in subcategory["subcategories"]:
                        if subsubcategory["name"] == "VIEW ALL":
                            if subsubcategory["isRedirected"]:
                                categoryId = subsubcategory["redirectCategoryId"]
                            else:
                                categoryId = subsubcategory["id"]


    resp = requests.get(f'https://www.zara.com/nl/en/category/{categoryId}/products?ajax=true', headers=headers)
    data = resp.json()
    
    product_names = []
    for element in data["productGroups"][0]["elements"]:
        for product in element["commercialComponents"]:
            if "oldPrice" in product and product["oldPrice"] > product["price"]:
                stripped_product = {}
                stripped_product["id"] = product["id"]
                stripped_product["brand"] = "zara"
                stripped_product["sectionName"] = product["sectionName"].lower()
                stripped_product["name"] = product["name"]
                stripped_product["oldPrice"] = product["oldPrice"]/100
                stripped_product["price"] = product["price"]/100
                stripped_product["displayDiscountPercentage"] = int(((product["oldPrice"] - product["price"]) / product["oldPrice"]) * 100)
                stripped_product["url"] = product["detail"]["colors"][0]["xmedia"][0]["url"]
                product_names.append(stripped_product)
                
    return product_names