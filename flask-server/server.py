from flask import Flask, jsonify
from search.mobile_de import search_vehicle

app = Flask(__name__)


@app.route('/cars')
def cars():
    cars = search_vehicle("car", "Ford", "Kuga", "500", "suv", "ST LINE X", "plug_in", "224", "251", "automatic")
    print(cars)
    return jsonify(cars)

if __name__ == '__main__':
    app.run(debug=True)