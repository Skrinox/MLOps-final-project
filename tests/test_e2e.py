import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app import app

class DummyE2EModel:
    def predict(self, df):
        # Simulates returning a predicted stock price
        return [150.25] 

@patch("backend.app.mlflow.pyfunc.load_model")
def test_e2e_prediction_flow(mock_load_model):

    # Inject our fake model into the application's startup process
    mock_load_model.return_value = DummyE2EModel()
    
    # Using 'with TestClient' ensures the FastAPI lifespan events (startup/shutdown) run
    with TestClient(app) as client:
        
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "ok"
        
        payload = {
            "Open": 145.0,
            "High": 150.0,
            "Low": 144.0,
            "Volume": 1000000
        }
        predict_response = client.post("/predict", json=payload)
        
        assert predict_response.status_code == 200
        data = predict_response.json()
        
        assert "predicted_close_price" in data
        assert data["predicted_close_price"] == 150.25
        assert "model_version_stage" in data