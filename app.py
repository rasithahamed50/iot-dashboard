from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    temperature = random.randint(25, 40)
    humidity = random.randint(40, 80)

    status = "Normal"
    if temperature > 35:
        status = "High Temperature ⚠️"

    return render_template("index.html", temp=temperature, hum=humidity, status=status)


@app.route('/data')
def get_data():
    return jsonify({
        "temp": random.randint(25, 40)
    })


if __name__ == '__main__':
    app.run(debug=True)