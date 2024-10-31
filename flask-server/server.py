from flask import Flask, jsonify
from search.zara import gather_items

app = Flask(__name__)


@app.route('/products')
def products():
    products = gather_items()
    print(products)
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)