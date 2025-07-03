# ml/utils.py
import os
import numpy as np
import pandas as pd
import yfinance as yf

from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from decouple import config

MODEL_PATH = config("MODEL_PATH", default="ml/stock_prediction_model.keras")

def load_stock_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    return load_model(MODEL_PATH)

def fetch_stock_data(ticker, period="1y", interval="1d"):
    df = yf.download(ticker, period=period, interval=interval)
    if df.empty:
        raise ValueError(f"No data found for {ticker}")
    return df[['Close']]

def prepare_data(df):
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(df)

    X, y = [], []
    for i in range(60, len(data_scaled)):
        X.append(data_scaled[i - 60:i, 0])
        y.append(data_scaled[i, 0])

    X = np.array(X)
    y = np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    return X, y, scaler

def predict_next_price(ticker):
    df = fetch_stock_data(ticker)
    X, y, scaler = prepare_data(df)

    model = load_stock_model()
    y_pred = model.predict(X)
    y_pred_rescaled = scaler.inverse_transform(y_pred)
    y_actual_rescaled = scaler.inverse_transform(y.reshape(-1, 1))

    next_input = df[-60:]['Close'].values.reshape(-1, 1)
    next_input_scaled = scaler.transform(next_input)
    next_input_scaled = next_input_scaled.reshape((1, 60, 1))
    next_pred_scaled = model.predict(next_input_scaled)
    next_price = scaler.inverse_transform(next_pred_scaled)[0][0]

    mse = mean_squared_error(y_actual_rescaled, y_pred_rescaled)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_actual_rescaled, y_pred_rescaled)

    return {
        "ticker": ticker,
        "next_day_price": round(next_price, 2),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4)
    }