from flask import Flask, jsonify
from flask_cors import CORS
from search.hm_men import gather_items

app = Flask(__name__)
CORS(app)

@app.route('/api/products', methods=['GET'])
def products():
    products = gather_items()
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True, port=8080)