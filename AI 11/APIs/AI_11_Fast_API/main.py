import traceback

import joblib
from fastapi import FastAPI, HTTPException

import pandas as pd
from pathlib import Path

from pydantic import BaseModel

app = FastAPI(
    title ="Price Prediction AI Service API"
)

MODEL_PATH = Path('../../models/model.pkl')
print("Model path:", MODEL_PATH)
print("File exists:", MODEL_PATH.exists())
try:
    loaded = joblib.load(MODEL_PATH)
    if isinstance(loaded, dict) and 'pipeline' in loaded:
        BUNDLE = loaded
        PIPLINE = BUNDLE['pipeline']
        FEATURES = BUNDLE.get('featured_order', ['Bedrooms', 'Bathrooms', 'Sqm', 'City'])
    print(f'Model loaded successfully {MODEL_PATH}')
except Exception as e:
    print(f'Failed to load model from {MODEL_PATH}')
    BUNDLE = None
    PIPLINE = None
    FEATURES = ['Bedrooms', 'Bathrooms', 'Sqm', 'City']

class PredictIn(BaseModel):
    bedrooms: float
    bathrooms: float
    sqm: float
    city: str


@app.post("/predict")
async def predict(request: PredictIn):
    print(PIPLINE)
    if PIPLINE is None:
        raise HTTPException(status_code=50, detail="No model loaded")
    try:
        features = {
            'Bedrooms': [request.bedrooms],
            'Bathrooms': [request.bathrooms],
            'Sqm': [request.sqm],
            'City': [request.city]
        }
        if 'Sqm' in FEATURES:
            features['Sqm'] = [request.sqm]
        features_df = pd.DataFrame(features, columns=FEATURES)
        prediction = PIPLINE.predict(features_df)[0]
        return {'priceAZN': float(prediction)}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/retrain')
async def retrain():
    pass
