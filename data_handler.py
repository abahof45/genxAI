import pandas as pd

def load_data(file_path="data.csv"):
    df = pd.read_csv(file_path)
    X = df.drop("target", axis=1).values
    y = df["target"].values
    return X, y