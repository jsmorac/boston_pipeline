# src/detect_and_retrain.py

import pandas as pd
import os
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric
from config import DATA_PATH
from train import train

def detect_drift(reference_path: str, current_path: str, output_path: str = "reports/drift_report.html") -> bool:
    reference_data = pd.read_csv(reference_path).drop(columns=["medv"], errors="ignore")
    current_data = pd.read_csv(current_path).drop(columns=["medv"], errors="ignore")

    # Crear el reporte de drift
    report = Report(metrics=[DatasetDriftMetric()])
    report.run(reference_data=reference_data, current_data=current_data)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    report.save_html(output_path)
    print(f"Reporte HTML generado: {output_path}")

    # Extraer el resultado
    result = report.as_dict()
    drift = result["metrics"][0]["result"]["dataset_drift"]
    print(f"¿Drift detectado?: {drift}")

    return drift

if __name__ == "__main__":
    new_data_path = "data/BostonHousing_drifted.csv"
    if detect_drift(DATA_PATH, new_data_path):
        print("⚠️ Drift detectado. Ejecutando reentrenamiento...")
        train()
    else:
        print("Sin drift significativo. No se ejecuta reentrenamiento.")
