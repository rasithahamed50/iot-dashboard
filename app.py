from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html",
                           temp=random.randint(25, 35),
                           hum=random.randint(40, 80))

@app.route('/data')
def data():
    return jsonify({
        "temp": random.randint(25, 35),
        "hum": random.randint(40, 80)
    })

if __name__ == "__main__":
    app.run(debug=True)
