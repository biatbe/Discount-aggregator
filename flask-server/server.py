from flask import Flask, jsonify
from flask_cors import CORS
from search.mango_men import gather_items as gather_mango_men_items
from search.mango_women import gather_items as gather_mango_women_items
from search.zara_men import gather_items as gather_zara_men_items
from search.zara_women import gather_items as gather_zara_women_items
from db.queries import store_products, get_all_products

app = Flask(__name__)
CORS(app)

@app.route('/api/products/update', methods=['GET'])
def products_update():
    products = []
    mango_men = gather_mango_men_items()
    mango_women = gather_mango_women_items()
    zara_men = gather_zara_men_items()
    zara_women = gather_zara_women_items()
    products.append(mango_men)
    products.append(mango_women)
    products.append(zara_men)
    products.append(zara_women)

    for product in products:
        store_products(product)

    return jsonify("SUCCESS")

@app.route('/api/products', methods=['GET'])
def all_products():
    products = get_all_products()
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True, port=8080)