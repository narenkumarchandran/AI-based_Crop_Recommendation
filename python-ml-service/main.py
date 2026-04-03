from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Farmer's Friend ML Service", description="Crop recommendation ML Microservice")

# Enable CORS for the Node API and any local tests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the ML Model
MODEL_PATH = "crop_recommendation_model.joblib"
model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
        logger.info(f"Successfully loaded model from {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        # Note: Depending on deployment, you might want to exit here if the model is critical

class CropFeatures(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict-crop")
def predict_crop(features: CropFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="ML Model is not loaded")
    
    try:
        # The RandomForestClassifier expects a 2D array / DataFrame matching training shape
        input_data = pd.DataFrame([features.dict()])
        prediction = model.predict(input_data)[0]
        
        return {"recommendation": str(prediction)}
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
