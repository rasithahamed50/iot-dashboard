"""
AURA - Ambient Unified Real-time Analytics
Flask Backend

Install : pip install flask flask-cors
Run     : python app.py
Open    : http://127.0.0.1:5000
"""

import time
import math
import random
import json
import threading
from datetime import datetime
from flask import Flask, jsonify, Response, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)

# ---------- sensor state ----------
_start = time.time()
_lock  = threading.Lock()

state = {
    "temperature": 22.0,
    "humidity":    55.0,
    "pressure":    1013.0,
    "aqi":         42.0,
    "light":       320.0,
    "noise":       38.0,
    "points":      0,
}

session = {
    "temp_max": 22.0,
    "temp_min": 22.0,
    "hum_sum":  55.0,
    "aqi_max":  42.0,
}


def _walk(val, lo, hi, step):
    val += random.uniform(-step, step)
    return max(lo, min(hi, val))


def _r(v):
    return round(v * 10) / 10


def sensor_loop():
    """Background thread: update readings every 5 seconds."""
    while True:
        time.sleep(5)
        with _lock:
            osc = math.sin(time.time() / 120) * 2

            state["temperature"] = _r(_walk(state["temperature"] + osc * 0.1, 10, 45, 0.4))
            state["humidity"]    = _r(_walk(state["humidity"],    20, 95,   1.0))
            state["pressure"]    = _r(_walk(state["pressure"],   980, 1040, 0.5))
            state["aqi"]         = _r(_walk(state["aqi"],          0, 200,  2.5))
            state["light"]       = _r(_walk(state["light"],        0, 1200, 25.0))
            state["noise"]       = _r(_walk(state["noise"],       25, 95,   1.5))
            state["points"]     += 1

            t = state["temperature"]
            if t > session["temp_max"]:
                session["temp_max"] = t
            if t < session["temp_min"]:
                session["temp_min"] = t
            session["hum_sum"] += state["humidity"]
            if state["aqi"] > session["aqi_max"]:
                session["aqi_max"] = state["aqi"]


threading.Thread(target=sensor_loop, daemon=True).start()


# ---------- helpers ----------
def build_payload():
    with _lock:
        pts   = max(state["points"], 1)
        h_avg = _r(session["hum_sum"] / pts)
        return {
            "timestamp":   datetime.now().isoformat(timespec="seconds"),
            "uptime":      round(time.time() - _start),
            "temperature": state["temperature"],
            "humidity":    state["humidity"],
            "pressure":    state["pressure"],
            "aqi":         state["aqi"],
            "light":       state["light"],
            "noise":       state["noise"],
            "points":      state["points"],
            "session": {
                "temp_max": session["temp_max"],
                "temp_min": session["temp_min"],
                "hum_avg":  h_avg,
                "aqi_max":  session["aqi_max"],
            },
        }


# ---------- routes ----------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/sensors")
def sensors():
    return jsonify(build_payload())


@app.route("/api/stream")
def stream():
    def generate():
        while True:
            yield "data: " + json.dumps(build_payload()) + "\n\n"
            time.sleep(5)
    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "uptime": round(time.time() - _start)})


# ---------- main ----------
if __name__ == "__main__":
    print("\n  AURA backend starting...")
    print("  Dashboard  ->  http://127.0.0.1:5000")
    print("  API JSON   ->  http://127.0.0.1:5000/api/sensors")
    print("  SSE stream ->  http://127.0.0.1:5000/api/stream\n")
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
