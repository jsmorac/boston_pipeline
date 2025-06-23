from fastapi import FastAPI, Request
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

from api.schema import HouseData
from api.predict_utils import load_model, make_prediction

app = FastAPI(title="Boston Housing Predictor")

# === MÉTRICAS ===
REQUEST_COUNT = Counter("request_count", "Número de peticiones a la API", ["endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Tiempo de respuesta", ["endpoint"])
PREDICTION_AVERAGE = Gauge("prediction_average", "Promedio del valor predicho más reciente")
PREDICTION_RANGE_LOW = Counter("prediction_range_low", "Predicciones menores a 20")
PREDICTION_RANGE_MID = Counter("prediction_range_mid", "Predicciones entre 20 y 30")
PREDICTION_RANGE_HIGH = Counter("prediction_range_high", "Predicciones mayores a 30")

# === MODELO ===
model = load_model()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de predicción de precios de vivienda"}

@app.post("/predict")
def predict_price(data: HouseData, request: Request):
    start_time = time.time()
    input_dict = data.dict()
    prediction = make_prediction(model, input_dict)
    PREDICTION_AVERAGE.set(prediction)

    if prediction < 20:
        PREDICTION_RANGE_LOW.inc()
    elif 20 <= prediction <= 30:
        PREDICTION_RANGE_MID.inc()
    else:
        PREDICTION_RANGE_HIGH.inc()
        
    duration = time.time() - start_time

    # Registrar métricas
    REQUEST_COUNT.labels(endpoint="/predict").inc()
    REQUEST_LATENCY.labels(endpoint="/predict").observe(duration)

    return {"predicted_price": prediction}

# === ENDPOINT DE MÉTRICAS ===
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
