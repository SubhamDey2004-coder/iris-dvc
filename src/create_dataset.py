from sklearn.datasets import load_iris
import pandas as pd


iris = load_iris()

df = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

df["target"] = iris.target

df.to_csv("data/raw/iris.csv", index=False)

print("Dataset created successfully!")
print(df.head())
print(f"Shape: {df.shape}")