import pytest
from fastapi.testclient import TestClient

# Import the module so we can override the global mlflow_model variable for testing
import backend.app as app_module
from backend.app import app, StockFeatures

client = TestClient(app)

class MockModel:
    def predict(self, df):
        return [155.50]
    
def test_stock_features_schema_valid():
    """Test that the Pydantic schema correctly parses valid stock data."""
    valid_data = {
        "Open": 150.50,
        "High": 155.00,
        "Low": 149.00,
        "Volume": 1200000
    }
    # If this fails, it throws a ValidationError
    feature_model = StockFeatures(**valid_data)
    
    assert feature_model.Open == 150.50
    assert feature_model.Volume == 1200000.0

def test_health_check_no_model():
    app_module.mlflow_model = None 
    response = client.get("/health")
    
    assert response.status_code == 503
    assert "Model not loaded" in response.json()["detail"]


def test_health_check_with_model():
    app_module.mlflow_model = MockModel() 
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "model" in response.json()

def test_predict_endpoint_success():
    app_module.mlflow_model = MockModel() 
    
    payload = {
        "Open": 150.0,
        "High": 160.0,
        "Low": 145.0,
        "Volume": 1200000
    }
    
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_close_price"] == 155.50 
    assert "model_version_stage" in data