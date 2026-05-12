# Import necessary libraries
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load models
with open('svm_model.pkl', 'rb') as f:
    svm_model = pickle.load(f)

with open('rf_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)

# Create a FastAPI app
app = FastAPI()

# Define a request body model
class DiabetesPredictionRequest(BaseModel):
    Pregnancies: float
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: float

# Define a response model
class DiabetesPredictionResponse(BaseModel):
    prediction: int
    probability: float

# Define a route for predictions
@app.post("/predict", response_model=DiabetesPredictionResponse)
def predict(request: DiabetesPredictionRequest):
    # Create a numpy array from the request body
    input_data = np.array([[
        request.Pregnancies,
        request.Glucose,
        request.BloodPressure,
        request.SkinThickness,
        request.Insulin,
        request.BMI,
        request.DiabetesPedigreeFunction,
        request.Age
    ]])

    # Standardize features
    scaler = StandardScaler()
    input_data = scaler.fit_transform(input_data)

    # Make predictions
    prediction_svm = svm_model.predict(input_data)
    prediction_rf = rf_model.predict(input_data)

    # Return the prediction and probability
    return {
        "prediction": prediction_rf[0],
        "probability": rf_model.predict_proba(input_data)[0][1]
    }