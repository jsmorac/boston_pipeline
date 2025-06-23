# src/config.py

import os
from dotenv import load_dotenv

# Cargar archivo .env
load_dotenv()

# Variables de entorno con valores por defecto
DATA_PATH = os.getenv("DATA_PATH", "data/BostonHousing.csv")
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")
METRICS_PATH = os.getenv("METRICS_PATH", "models/metrics.json")
SELECTED_MODEL = os.getenv("SELECTED_MODEL", "random_forest")
