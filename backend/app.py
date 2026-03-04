import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import mlflow.pyfunc
from fastapi.middleware.cors import CORSMiddleware

MODEL_NAME = os.getenv("MODEL_NAME", "ToyotaStockPredictor")
MODEL_STAGE = os.getenv("MODEL_STAGE", "Staging") 
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "")

mlflow_model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function to load the model at start."""
    global mlflow_model
    print(f"Loading {MODEL_NAME} from stage: {MODEL_STAGE}")
    
    tracking_uri = MLFLOW_TRACKING_URI
    print(f"Using MLflow tracking URI: {tracking_uri}")
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)

    try:
        model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
        print(f"Attempting to load model from URI: {model_uri}")
        mlflow_model = mlflow.pyfunc.load_model(model_uri)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
    
    yield 

    print("Shutting down.")


app = FastAPI(title="Toyota stock predictor", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockFeatures(BaseModel):
    Open: float
    High: float
    Low: float
    Volume: float


@app.get("/health")
def health():
    if mlflow_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    return {"status": "ok", "model": MODEL_NAME, "stage": MODEL_STAGE}


@app.post("/predict")
def predict_stock_price(features: StockFeatures):
    """
    Takes stock features and returns the predicted close price.
    """
    
    if mlflow_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    
    try:
        input_data = pd.DataFrame([features.dict()])
        prediction = mlflow_model.predict(input_data)
        
        return {
            "predicted_close_price": float(prediction[0]),
            "model_version_stage": MODEL_STAGE
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

 
@app.options("/predict")
def options_predict():
    return {
        "methods": ["POST"],
        "description": "Endpoint to predict the close price of Toyota stock based on input features."
    }