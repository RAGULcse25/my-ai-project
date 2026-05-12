# Import required libraries
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from data_loader import load_data
from model import train_model

# Create a FastAPI application instance
app = FastAPI()

# Define a request body model for prediction
class PredictionRequest(BaseModel):
    features: list[float]

# Load the dataset
data = load_data()

# Train the machine learning model
model = train_model(data)

# Define a route for model training
@app.post("/train")
async def train():
    # Train the model on the loaded data
    global model
    model = train_model(data)
    return {"message": "Model trained successfully"}

# Define a route for prediction
@app.post("/predict")
async def predict(request: PredictionRequest):
    # Use the trained model to make a prediction
    prediction = model.predict([request.features])
    return {"prediction": prediction[0]}

# Define a route for model evaluation
@app.get("/evaluate")
async def evaluate():
    # Evaluate the model on the test data
    X_train, X_test, y_train, y_test = train_test_split(data.drop("target", axis=1), data["target"], test_size=0.2, random_state=42)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return {"accuracy": accuracy}

# Define a route for data loading
@app.get("/data")
async def get_data():
    # Return the loaded data
    return {"data": data.head().to_dict(orient="records")}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)