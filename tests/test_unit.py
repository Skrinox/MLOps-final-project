import pytest
from backend.app import app, StockFeatures
import pandas as pd

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

def test_stock_features_schema_invalid_type():
    """Volume must be a float, not a string."""
    invalid_data = {
        "Open": 150.0,
        "High": 160.0,
        "Low": 145.0,
        "Volume": "not_a_number"
    }

    with pytest.raises(Exception):
        StockFeatures(**invalid_data)

def test_stock_features_schema_fields():
    """Ensure schema exposes the correct fields."""
    feature = StockFeatures(
        Open=100.0,
        High=110.0,
        Low=95.0,
        Volume=500000
    )

    fields = feature.dict().keys()

    assert "Open" in fields
    assert "High" in fields
    assert "Low" in fields
    assert "Volume" in fields

def test_prediction_output_format():
    """Prediction should be convertible to float."""
    model = MockModel()

    df = pd.DataFrame([{
        "Open": 120.0,
        "High": 125.0,
        "Low": 118.0,
        "Volume": 800000
    }])

    prediction = model.predict(df)

    result = float(prediction[0])

    assert isinstance(result, float)