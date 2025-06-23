# README: Boston Housing Prediction API

Este repositorio contiene una solución completa de machine learning para predecir precios de vivienda usando el dataset **Boston Housing**. Incluye entrenamiento de modelos, exposición como API REST, monitoreo con Prometheus, visualización con Grafana y detección de drift con Evidently.

---

## Tabla de Contenidos

- [1. Requisitos](#1-requisitos)
- [2. Instalación local](#2-instalación-local)
- [3. Entrenamiento del modelo](#3-entrenamiento-del-modelo)
- [4. Despliegue de la API con Docker](#4-despliegue-de-la-api-con-docker)
- [5. Documentación de la API](#5-documentación-de-la-api)
- [6. Monitoreo y métricas](#6-monitoreo-y-métricas)
- [7. Visualización en Grafana](#7-visualización-en-grafana)
- [7.1. Detección de Drift (Bonus)](#71-detección-de-drift-bonus)
- [8. Estructura del proyecto](#8-estructura-del-proyecto)
- [9. Trabajo futuro](#9-trabajo-futuro)

---

## 1. Requisitos

- Python 3.9 o superior
- Docker y Docker Compose
- Navegador web (para ver API Docs y Grafana)

---

## 2. Instalación local

1. Clona el repositorio:

```bash
git clone https://github.com/jsmorac/boston_pipeline.git
cd boston_pipeline
```

2. Crea entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Configura el archivo `.env` (ya está incluido):

```env
DATA_PATH=data/BostonHousing.csv
MODEL_PATH=models/model.pkl
METRICS_PATH=models/metrics.json
SELECTED_MODEL=random_forest
```

---

## 3. Entrenamiento del modelo

Ejecuta:

```bash
python src/train.py
```

Esto:

- Carga los datos
- Entrena uno de los 4 modelos disponibles
- Evalúa con MAE y R²
- Guarda el modelo en `models/`
- Registra todo en MLflow

Puedes cambiar el modelo editando `.env` con:

- `linear`
- `ridge`
- `knn`
- `random_forest`

---

## 4. Despliegue de la API con Docker

### Paso 1: Construir y levantar servicios

```bash
docker compose up --build
```

Esto levanta:

- API (`localhost:8000`)
- Prometheus (`localhost:9090`)
- Grafana (`localhost:3000`)

### Paso 2: Acceder a los servicios

- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3000](http://localhost:3000)  
  Login: `admin` / `admin`

---

## 5. Documentación de la API

Disponible automáticamente en `http://localhost:8000/docs`

### Endpoints principales:

- `POST /predict` → Recibe datos y devuelve el precio estimado
- `GET /metrics` → Expone métricas para Prometheus

Ejemplo de JSON válido:

```json
{
  "crim": 0.02,
  "zn": 0.0,
  "indus": 7.0,
  "chas": 0,
  "nox": 0.47,
  "rm": 6.5,
  "age": 65.2,
  "dis": 4.5,
  "rad": 4,
  "tax": 300.0,
  "ptratio": 18.0,
  "b": 390.5,
  "lstat": 9.0
}
```

---

## 6. Monitoreo y métricas

La API expone métricas a través de `/metrics` y Prometheus las recoge automáticamente. Métricas incluidas:

- `request_count_total`: número de peticiones
- `request_latency_seconds`: latencia de la API
- `prediction_average`: promedio de predicciones
- Rango de predicciones:
  - `< 20` → `prediction_range_low_total`
  - `20 - 30` → `prediction_range_mid_total`
  - `> 30` → `prediction_range_high_total`

---

## 7. Visualización en Grafana

1. Ir a [http://localhost:3000](http://localhost:3000)
2. Iniciar sesión con:
   - Usuario: `admin`
   - Contraseña: `admin`
3. Crear un panel de tipo `Time Series`
4. Agrega las siguientes métricas:
   - `rate(request_count_total[1m])` → Tasa de peticiones
   - `prediction_average` → Precio promedio
   - `prediction_range_low_total`, `mid`, `high`
   - `histogram_quantile(0.95, rate(request_latency_seconds_bucket[1m]))` → Latencia P95

---

## 7.1. Detección de Drift (Bonus)

Este proyecto incluye una funcionalidad de detección de drift usando la librería **Evidently AI**. El análisis compara un dataset actual con el dataset base y genera un reporte HTML interactivo.

### ¿Cómo generar el reporte?

1. Crear un dataset con cambios simulados:

```bash
python src/generate_drifted_data.py
```

2. Ejecutar el análisis de drift:

```bash
python src/detect_and_retrain.py
```

Esto genera un archivo en:

```
reports/drift_report.html
```

### ¿Qué hace el sistema si detecta drift?

- Analiza si las variables tienen cambios significativos en distribución.
- Si el drift es alto, se muestra el resultado en consola.
- **Nota:** El sistema actualmente no reentrena automáticamente con datos nuevos, pero se puede modificar fácilmente para hacerlo.

---

## 8. Estructura del proyecto

```
├── api
│   ├── main.py             # FastAPI App
│   ├── schema.py           # Validación con Pydantic
│   └── predict_utils.py    # Predicción y escalado
├── src
│   ├── config.py           # Variables de entorno
│   ├── train.py            # Entrenamiento y MLflow
│   ├── utils.py            # Utilidades de IO
│   ├── generate_drifted_data.py  # Simulación de drift
│   └── detect_and_retrain.py     # Análisis y acción
├── models                  # Modelos y métricas guardadas
├── data                    # Dataset original y drifted
├── reports                 # Reporte HTML generado por Evidently
├── prometheus
│   └── prometheus.yml      # Configuración del scraping
├── docker-compose.yml      # Orquestación de servicios
├── Dockerfile              # Imagen de la API
└── .env                    # Variables configurables
```

---

## 9. Trabajo futuro

- Integrar reentrenamiento con datasets nuevos al detectar drift
- Envío de alertas en Prometheus (vía alertmanager)
- Autenticación en la API para entornos productivos
- Despliegue en Azure (AKS, App Service o Container Instances)

---

¡Gracias! 
