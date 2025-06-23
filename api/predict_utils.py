# api/predict_utils.py

import joblib
import numpy as np
import pandas as pd

MODEL_PATH = "models/model.pkl"

def load_model():
    return joblib.load(MODEL_PATH)  # devuelve dict con model y scaler

def make_prediction(model_bundle, input_data: dict):
    df = pd.DataFrame([input_data])

    model = model_bundle["model"]
    scaler = model_bundle["scaler"]

    # Aplicar escalado si hay scaler
    if scaler is not None:
        df = scaler.transform(df)

    prediction = model.predict(df)
    return float(prediction[0])
