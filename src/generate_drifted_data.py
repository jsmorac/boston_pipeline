# src/generate_drifted_data.py
import pandas as pd
import numpy as np
from config import DATA_PATH

df = pd.read_csv(DATA_PATH)

np.random.seed(42)
df_drifted = df.copy()
df_drifted["crim"] *= np.random.uniform(1.5, 2.0, size=len(df))
df_drifted["nox"] += np.random.normal(0.05, 0.01, size=len(df))
df_drifted["rm"] -= np.random.normal(0.5, 0.1, size=len(df))
df_drifted["age"] += np.random.normal(10, 5, size=len(df))

df_drifted.to_csv("data/BostonHousing_drifted.csv", index=False)
print("Dataset con drift guardado.")
