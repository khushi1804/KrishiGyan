from flask import Flask, request, jsonify, make_response
from werkzeug.serving import run_simple
import pickle
import numpy as np
import pandas as pd
import datetime
from flask_cors import CORS
import random
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)
CORS(app)

# Load the crop trained model
with open("model.pkl", "rb") as f:
    crop_model = pickle.load(f)

model = crop_model["model"]
encoders = crop_model["encoders"]

SOIL_NPK_VALUES = {
    "sandy": {"N": (10, 60), "P": (5, 30), "K": (10, 50), "ph": (5.5, 6.5)},
    "clay": {"N": (40, 120), "P": (10, 50), "K": (20, 80), "ph": (6.0, 7.5)},
    "loamy": {"N": (50, 150), "P": (15, 60), "K": (30, 100), "ph": (6.2, 7.2)},
    "peaty": {"N": (20, 100), "P": (5, 40), "K": (15, 70), "ph": (4.5, 6.0)},
    "saline": {"N": (5, 40), "P": (3, 20), "K": (10, 50), "ph": (7.5, 9.0)},
    "chalky": {"N": (15, 80), "P": (5, 35), "K": (20, 90), "ph": (7.0, 8.5)}
}

def get_soil_npk(soil_type):
    if soil_type in SOIL_NPK_VALUES:
        npk_range = SOIL_NPK_VALUES[soil_type]
    else:
        npk_range = {"N": (20, 100), "P": (10, 50), "K": (20, 80), "ph": (5.5, 7.5)}

    return {
        'N': random.randint(*npk_range["N"]),
        'P': random.randint(*npk_range["P"]),
        'K': random.randint(*npk_range["K"]),
        'ph': round(random.uniform(*npk_range["ph"]), 2)
    }

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    if not model:
        return jsonify({'error': 'Model not loaded properly'}), 500

    try:
        data = request.json
        required_fields = ['soil_type', 'weather', 'humidity', 'rainfall']

        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required input fields'}), 400

        current_month = datetime.datetime.now().month
        
        soil_type = data['soil_type'].lower()

        npk_values = get_soil_npk(soil_type)

        features = [
            npk_values['N'], npk_values['P'], npk_values['K'],
            float(data['weather']), float(data['humidity']),
            npk_values['ph'], float(data['rainfall']), current_month
        ]

        prediction = model.predict([np.array(features)])
        return jsonify({'prediction': str(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City not provided"}), 400

    if not WEATHER_API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    try:
        url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return jsonify({
            "temp_c": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"]
        })

    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch weather data: {str(e)}"}), 500


if __name__ == '__main__':
    run_simple('localhost', 5000, app)
