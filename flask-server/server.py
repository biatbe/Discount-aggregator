from flask import Flask

app = Flask(__name__)


@app.route('/cars')
def cars():
    return {"cars": ["Car1", "Car2"]}

if __name__ == '__main__':
    app.run(debug=True)