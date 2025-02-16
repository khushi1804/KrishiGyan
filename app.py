from flask import Flask, request, jsonify, make_response
from werkzeug.serving import run_simple
import pickle
import numpy as np
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Load trained models
try:
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
except Exception as e:
    print(f"Error loading model.pkl: {e}")
    model = None

try:
    with open("model_irrigation.pkl", "rb") as f:
        irrigation_model = pickle.load(f)
        rf_model = irrigation_model.get("model")
        label_encoders = irrigation_model.get("encoders")
except Exception as e:
    print(f"Error loading model_irrigation.pkl: {e}")
    rf_model = None
    label_encoders = None

# Constant file with dummy values for N, P, K based on soil type
SOIL_NPK_VALUES = {
    "sandy": {"N": 10, "P": 5, "K": 8, "ph":7.03},
    "clay": {"N": 15, "P": 10, "K": 12,"ph": 6.56},
    "loamy": {"N": 20, "P": 15, "K": 18, "ph": 5.87},
    "silt": {"N": 12, "P": 8, "K": 10,"ph":5.34}
}


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.route('/predict', methods=['OPTIONS', 'POST'])
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
        required_fields = ['soil_type', 'weather', 'humidity','rainfall']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required input fields'}), 400
        
        soil_type = data['soil_type'].lower()
        npk_values = SOIL_NPK_VALUES.get(soil_type)
        
        features = [npk_values['N'], npk_values['P'], npk_values['K'],data['weather'],data['humidity'],npk_values['ph'],data['rainfall']]
        prediction = model.predict([np.array(features)])
        return jsonify({'prediction': str(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

    
# @app.route('/predict_irrigation', methods=['OPTIONS', 'POST'])
# def predict_irrigation():
#     if request.method == 'OPTIONS':
#         response = make_response()
#         response.headers["Access-Control-Allow-Origin"] = "*"
#         response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
#         response.headers["Access-Control-Allow-Headers"] = "Content-Type"
#         return response
    
#     if not rf_model or not label_encoders:
#         return jsonify({'error': 'Irrigation model not loaded properly'}), 500
    
#     try:
#         data = request.json.get('features', [])
#         col_names = ["Soil_Moisture(%)", "Rainfall(mm)", "Evapotranspiration(mm/day)", "Soil_Type", "Crop_Stage", "Temperature(°C)", "Humidity(%)", "Water_Table_Depth(m)"]
        
#         if not isinstance(data, list) or len(data) != len(col_names):
#             return jsonify({'error': 'Invalid input data'}), 400
        
#         input_df = pd.DataFrame([data], columns=col_names)

#         # Encode categorical variables
#         for col in ["Soil_Type", "Crop_Stage"]:
#             if col in label_encoders:
#                 input_df[col] = label_encoders[col].transform([input_df[col].values[0]])
#             else:
#                 return jsonify({'error': f'Missing label encoder for {col}'}), 500
        
#         prediction = rf_model.predict(input_df.values)
#         result = "Yes" if prediction[0] == 1 else "No"
#         return jsonify({'prediction': result})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    run_simple('localhost', 5000, app)