from flask import Flask, jsonify
from flask_cors import CORS
from search.mango_men import gather_items as gather_mango_men_items
from search.mango_women import gather_items as gather_mango_women_items
from search.zara_men import gather_items as gather_zara_men_items
from search.zara_women import gather_items as gather_zara_women_items
from search.massimo_dutti_men import gather_items as gather_massimo_dutti_men_items
from db.queries import store_products, get_all_products, clear_products

app = Flask(__name__)
CORS(app)

@app.route('/api/products/update', methods=['GET'])
def products_update():
    # Clear all products before inserting new discounts
    # Previous week's discounts might not be available anymore
    # clear_products()
    
    products = []
    # mango_men = gather_mango_men_items()
    # mango_women = gather_mango_women_items()
    # zara_men = gather_zara_men_items()
    # zara_women = gather_zara_women_items()
    massimo_dutti_men = gather_massimo_dutti_men_items()
    # products.append(mango_men)
    # products.append(mango_women)
    # products.append(zara_men)
    # products.append(zara_women)
    products.append(massimo_dutti_men)


    for product in products:
        store_products(product)

    return jsonify("SUCCESS")

@app.route('/api/products', methods=['GET'])
def all_products():
    products = get_all_products()
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True, port=8080)