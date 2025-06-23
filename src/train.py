# src/train.py

import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from config import DATA_PATH, MODEL_PATH, METRICS_PATH, SELECTED_MODEL
from utils import load_data, save_model, save_metrics

def get_model(name: str):
    if name == "linear":
        return LinearRegression()
    elif name == "ridge":
        return Ridge(alpha=1.0)
    elif name == "random_forest":
        return RandomForestRegressor(n_estimators=100, random_state=42)
    elif name == "knn":
        return KNeighborsRegressor(n_neighbors=5)
    else:
        raise ValueError(f"Modelo no soportado: {name}")

def train():
    mlflow.set_experiment("boston_regression")

    # 1. Cargar datos
    df = load_data(DATA_PATH)
    X = df.drop("medv", axis=1)
    y = df["medv"]

    # 2. Separar en train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 3. Escalado solo si el modelo lo requiere
    model = get_model(SELECTED_MODEL)
    needs_scaling = SELECTED_MODEL in ["linear", "ridge", "knn"]

    if needs_scaling:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
    else:
        scaler = None  # no se necesita

    # 4. Entrenamiento y evaluación
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    # 5. Log en consola
    print(f"[{SELECTED_MODEL.upper()}] MAE: {mae:.4f} | R²: {r2:.4f}")

    # 6. Guardado
    save_model({"model": model, "scaler": scaler}, MODEL_PATH)
    save_metrics({"mae": mae, "r2_score": r2}, METRICS_PATH)

    # 7. MLflow
    with mlflow.start_run():
        # Información general
        mlflow.log_param("model_type", SELECTED_MODEL)
        mlflow.log_param("n_samples", X.shape[0])
        mlflow.log_param("n_features", X.shape[1])

        # Hiperparámetros por modelo
        if SELECTED_MODEL == "random_forest":
            mlflow.log_param("n_estimators", model.n_estimators)
            mlflow.log_param("max_depth", model.max_depth)
        elif SELECTED_MODEL == "ridge":
            mlflow.log_param("alpha", model.alpha)
        elif SELECTED_MODEL == "knn":
            mlflow.log_param("n_neighbors", model.n_neighbors)
        elif SELECTED_MODEL == "linear":
            mlflow.log_param("fit_intercept", model.fit_intercept)

        # Métricas
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2_score", r2)

        # Modelo serializado
        mlflow.sklearn.log_model(model, "model")

if __name__ == "__main__":
    train()
