import os
import json
import time

import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

MODEL_NAME = os.getenv("MODEL_NAME", "ToyotaStockPredictor")

def main():
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "")
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
        token = os.environ.get("MLFLOW_TRACKING_TOKEN", "")
        if token:
            os.environ["MLFLOW_TRACKING_USERNAME"] = token
            os.environ["MLFLOW_TRACKING_PASSWORD"] = token

    # Load Data
    data_path = os.getenv("DATA_PATH", "data/Toyota_Stock_Prices_1980_2026.csv")
    df = pd.read_csv(data_path)
    
    features = ['Open', 'High', 'Low', 'Volume']
    target = 'Close'
    df = df.dropna(subset=features + [target])
    
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # train
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # eval
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    # log to mlflow
    run_name = f"candidate-{int(time.time())}"
    with mlflow.start_run(run_name=run_name) as run:
        
        # log metrics, params and versions (git and dvc)
        mlflow.log_metric("mse", float(mse))
        mlflow.log_metric("mae", float(mae))
        mlflow.log_metric("r2", float(r2))
        mlflow.log_param("model_type", "RandomForestRegressor")
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 10)
        mlflow.log_param("data_version", os.getenv("DATA_VERSION", "dvc:unknown"))
        mlflow.log_param("git_commit", os.getenv("GIT_COMMIT", "git:unknown"))
        mlflow.sklearn.log_model(model, artifact_path="model")
        
        model_uri = f"runs:/{run.info.run_id}/model"
        mv = mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)
        
        # for easy retrieval from the logs in the CI/CD pipeline
        out = {
            "run_id": run.info.run_id, 
            "mse": float(mse),
            "mae": float(mae),
            "r2": float(r2),
            "model_version": mv.version
        }
        print(json.dumps(out))

if __name__ == "__main__":
    main()