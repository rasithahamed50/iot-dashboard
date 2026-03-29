from flask import Flask, render_template, jsonify
import random
import time

app = Flask(__name__)

def get_sensor_data():
    temperature = round(random.uniform(22, 45), 1)
    humidity = round(random.uniform(30, 90), 1)
    pressure = round(random.uniform(980, 1030), 1)
    air_quality = round(random.uniform(0, 500), 1)
    return temperature, humidity, pressure, air_quality

@app.route('/')
def home():
    temperature, humidity, pressure, air_quality = get_sensor_data()

    alerts = []
    if temperature > 38:
        alerts.append({"type": "danger", "msg": f"Critical Temperature: {temperature}°C"})
    elif temperature > 35:
        alerts.append({"type": "warning", "msg": f"High Temperature: {temperature}°C"})

    if humidity > 80:
        alerts.append({"type": "warning", "msg": f"High Humidity: {humidity}%"})
    elif humidity < 35:
        alerts.append({"type": "warning", "msg": f"Low Humidity: {humidity}%"})

    if air_quality > 300:
        alerts.append({"type": "danger", "msg": f"Poor Air Quality: AQI {air_quality}"})
    elif air_quality > 150:
        alerts.append({"type": "warning", "msg": f"Moderate Air Quality: AQI {air_quality}"})

    return render_template(
        "index.html",
        temp=temperature,
        hum=humidity,
        pressure=pressure,
        aqi=air_quality,
        alerts=alerts
    )

@app.route('/data')
def get_data():
    temperature, humidity, pressure, air_quality = get_sensor_data()

    alerts = []
    if temperature > 38:
        alerts.append({"type": "danger", "msg": f"Critical Temperature: {temperature}°C"})
    elif temperature > 35:
        alerts.append({"type": "warning", "msg": f"High Temperature: {temperature}°C"})

    if humidity > 80:
        alerts.append({"type": "warning", "msg": f"High Humidity: {humidity}%"})
    elif humidity < 35:
        alerts.append({"type": "warning", "msg": f"Low Humidity: {humidity}%"})

    if air_quality > 300:
        alerts.append({"type": "danger", "msg": f"Poor Air Quality: AQI {air_quality}"})
    elif air_quality > 150:
        alerts.append({"type": "warning", "msg": f"Moderate Air Quality: AQI {air_quality}"})

    return jsonify({
        "temp": temperature,
        "hum": humidity,
        "pressure": pressure,
        "aqi": air_quality,
        "alerts": alerts,
        "timestamp": int(time.time())
    })

if __name__ == '__main__':
    app.run(debug=True)
