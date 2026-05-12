# Import required libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from data_loader import load_data
from model import train_model

# Initialize the FastAPI application
app = FastAPI()

# Define a request body model for prediction
class PredictionRequest(BaseModel):
    features: list[float]

# Load the dataset and train the model
data = load_data()
X_train, X_test, y_train, y_test = train_test_split(data.drop('target', axis=1), data['target'], test_size=0.2, random_state=42)
model = train_model(X_train, y_train)

# Define the API endpoint for prediction
@app.post("/predict")
async def predict(request: PredictionRequest):
    # Use the trained model to make a prediction
    prediction = model.predict([request.features])
    return JSONResponse(content={"prediction": int(prediction[0])}, media_type="application/json")

# Define the API endpoint for model evaluation
@app.get("/evaluate")
async def evaluate():
    # Evaluate the trained model using the test data
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return JSONResponse(content={"accuracy": accuracy}, media_type="application/json")

# Define the API endpoint for data information
@app.get("/data")
async def data_info():
    # Return information about the dataset
    return JSONResponse(content={"features": list(data.drop('target', axis=1).columns), "target": data['target'].name}, media_type="application/json")

# Define a root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the machine learning API"}