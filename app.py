from flask import Flask, request, jsonify, make_response
from werkzeug.serving import run_simple
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)


# Load the crop trained model
with open("model.pkl", "rb") as f:
    crop_model = pickle.load(f)

model = crop_model["model"]
encoders = crop_model["encoders"]

# Load the trained model
with open("model_irrigation.pkl", "rb") as f:
    irrigation_model = pickle.load(f)

rf_model = irrigation_model["model"]
label_encoders = irrigation_model["encoders"]

SOIL_NPK_VALUES = {
    "sandy": {"N": 10, "P": 5, "K": 8, "pH": 5.45},
    "clay": {"N": 15, "P": 10, "K": 12, "pH": 6.78},
    "loamy": {"N": 20, "P": 15, "K": 18, "pH": 7.45},
    "silt": {"N": 12, "P": 8, "K": 10, "pH": 6.87}
}

@app.route('/predict', methods=['GET','POST'])
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
        data = request.json['features']
        data[-1] = encoders.transform([data[-1]])[0]
        print('____',data)
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required input fields'}), 400
        
        soil_type = data['soil_type'].lower()
        npk_values = SOIL_NPK_VALUES.get(soil_type)
        
        features = [npk_values['N'], npk_values['P'], npk_values['K'],data['weather'],data['humidity'],npk_values['ph'],data['rainfall']]
        prediction = model.predict([np.array(features)])
        return jsonify({'prediction': str(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

    
@app.route('/predict_irrigation', methods=['OPTIONS', 'POST'])
def predict_irrigation():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    if not rf_model or not label_encoders:
        return jsonify({'error': 'Irrigation model not loaded properly'}), 500
    
    try:
        data = request.json.get('features', [])
        col_names = ["Soil_Moisture(%)", "Rainfall(mm)", "Evapotranspiration(mm/day)", "Soil_Type", "Crop_Stage", "Temperature(°C)", "Humidity(%)", "Water_Table_Depth(m)"]
        
        if not isinstance(data, list) or len(data) != len(col_names):
            return jsonify({'error': 'Invalid input data'}), 400
        
        input_df = pd.DataFrame([data], columns=col_names)

        # Encode categorical variables
        for col in ["Soil_Type", "Crop_Stage"]:
            if col in label_encoders:
                input_df[col] = label_encoders[col].transform([input_df[col].values[0]])
            else:
                return jsonify({'error': f'Missing label encoder for {col}'}), 500
        
        prediction = rf_model.predict(input_df.values)
        result = "Yes" if prediction[0] == 1 else "No"
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    run_simple('localhost', 5000, app)
