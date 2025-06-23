# src/utils.py

import pandas as pd
import os
import joblib
import json

def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def save_model(model, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)

def save_metrics(metrics: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(metrics, f, indent=4)
