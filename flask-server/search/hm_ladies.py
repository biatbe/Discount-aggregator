import requests

def gather_items():
    headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"}
    resp = requests.get("https://api.hm.com/search-services/v1/nl_NL/listing/resultpage?page=1&pageId=/ladies/last-chance/view-all&page-size=72&categoryId=LADIES_LASTCHANCE&touchPoint=DESKTOP&skipStockCheck=false", headers=headers)
    data = resp.json()

    total_pages = data["pagination"]["totalPages"]
    
    product_names = []
    for pageNum in range(1, total_pages + 1):
        resp = requests.get(f'https://api.hm.com/search-services/v1/nl_NL/listing/resultpage?page={pageNum}&pageId=/ladies/last-chance/view-all&page-size=72&categoryId=LADIES_LASTCHANCE&touchPoint=DESKTOP&skipStockCheck=false', headers=headers)
        data = resp.json()
        for product in data["plpList"]["productList"]:
            stripped_product = {}
            stripped_product["id"] = product["id"]
            stripped_product["brand"] = "H&M"
            stripped_product["sectionName"] = "women"
            stripped_product["name"] = product["productName"]
            prices = product["prices"]
            if prices[0]["priceType"] != "redPrice":
                continue
            stripped_product["price"] = prices[0]["price"]
            stripped_product["oldPrice"] = prices[1]["price"]
            if prices[0]["price"] > prices[1]["price"]:
                continue
            stripped_product["displayDiscountPercentage"] = int(((prices[1]["price"] - prices[0]["price"]) / prices[1]["price"]) * 100)
            stripped_product["url"] = product["swatches"][0]["productImage"]
            stripped_product["href"] = f'https://www2.hm.com{product["url"]}'
            product_names.append(stripped_product)

    return product_names