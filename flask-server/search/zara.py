import time
import requests
import json
from types import SimpleNamespace

def gather_items():
    headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"}
    resp = requests.get("https://www.zara.com/nl/en/category/2443335/products?ajax=true", headers=headers)
    data = resp.json()
    
    product_names = []
    for element in data["productGroups"][0]["elements"]:
        for product in element["commercialComponents"]:
            if "discountPercentage" in product:
                stripped_product = {}
                stripped_product["id"] = product["id"]
                stripped_product["sectionName"] = product["sectionName"]
                stripped_product["name"] = product["name"]
                stripped_product["oldPrice"] = product["oldPrice"]/100
                stripped_product["price"] = product["price"]/100
                stripped_product["displayDiscountPercentage"] = product["displayDiscountPercentage"]
                stripped_product["url"] = product["detail"]["colors"][0]["xmedia"][0]["url"]
                product_names.append(stripped_product)
                
    return product_names