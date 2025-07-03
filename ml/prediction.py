import joblib
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = joblib.load(MODEL_PATH)

def predict_stock(data):
    features = np.array([[data['open'], data['high'], data['low'], data['volume']]])  
    prediction = model.predict(features)
    return prediction[0]