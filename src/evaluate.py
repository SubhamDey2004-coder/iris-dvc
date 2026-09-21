import json
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score


test = pd.read_csv("data/test.csv")

X = test.drop(columns=["target"])
y = test["target"]

model = joblib.load("models/model.pkl")

predictions = model.predict(X)

accuracy = accuracy_score(y, predictions)

metrics = {
    "accuracy": accuracy
}

with open("metrics/metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print(f"Accuracy: {accuracy:.4f}")