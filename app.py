from flask import Flask, request, jsonify
from werkzeug.serving import run_simple
import pickle
import numpy as np
import pandas as pd
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Load trained model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


#Load the trained model
with open("model_irrigation.pkl", "rb") as f:
    irrigation_model = pickle.load(f)

# rf_model = irrigation_model["model"]
# label_encoders = irrigation_model["encoders"]

@app.route('/predict', methods=['POST'])
def predict():
    print('GOT CALL')
    #data = request.json  # Expecting a list of feature values
    data = request.json['features']
    print('____',data)
    prediction = model.predict([np.array(data)])  # Convert to NumPy array
    print(prediction[0])
    return jsonify({'prediction': str(prediction[0])})  # Return as JSON

# @app.route('/predict_irrigation', methods=['GET','POST'])
# def predict_irrigation():
#     print('GOT CALL IRRIGATION')
#     #data = request.json  # Expecting a list of feature values
#     data = request.json['features']
#     col_names = ["Soil_Moisture(%)" ,"Rainfall(mm)","Evapotranspiration(mm/day)","Soil_Type","Crop_Stage","Temperature(Â°C)","Humidity(%)","Water_Table_Depth(m)"]
#     input_df = pd.DataFrame([data],columns=col_names)
#     print('_INPUT DATA_',data)

#     # Encode categorical variables
#     for col in ["Soil_Type", "Crop_Stage"]:
#         input_df[col] = label_encoders[col].transform(input_df[col])

#     # Predict irrigation need
#     #print(input_df)
#     #print(input_df.values)
#     prediction = rf_model.predict(input_df.values)
#     result = "Yes" if prediction[0] == 1 else "No"

#     #prediction = model.predict([np.array(data)])  # Convert to NumPy array
#     #result = "Yes" if prediction[0] == 1 else "No"
#     print(result)
#     return jsonify({'prediction': result})


#if __name__ == '__main__':
#    app.run(debug=True)
#from flask import Flask

#app = Flask(__name__)
if __name__ == '__main__':
    run_simple('localhost', 5000, app)
