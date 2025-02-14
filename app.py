from flask import Flask, request, jsonify
from werkzeug.serving import run_simple
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/predict', methods=['GET','POST'])
def predict():
    print('GOT CALL')
    #data = request.json  # Expecting a list of feature values
    data = request.json['features']
    print('____',data)
    prediction = model.predict([np.array(data)])  # Convert to NumPy array
    print(prediction[0])
    return jsonify({'prediction': str(prediction[0])})  # Return as JSON

#if __name__ == '__main__':
#    app.run(debug=True)
#from flask import Flask

#app = Flask(__name__)
if __name__ == '__main__':
    run_simple('localhost', 5000, app)
