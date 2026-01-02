from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model(X, y):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def save_model(model, path="model.pkl"):
    joblib.dump(model, path)

def load_model(path="model.pkl"):
    return joblib.load(path)