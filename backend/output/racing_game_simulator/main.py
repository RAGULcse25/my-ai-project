# Import necessary libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from model import RacingGameModel
from data_loader import DataLoader
import uvicorn
import numpy as np
import pandas as pd
import json

# Initialize the FastAPI application
app = FastAPI()

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the dataset and create a data loader instance
data_loader = DataLoader()
data = data_loader.load_data()

# Train the machine learning model
model = RacingGameModel()
model.train(data)

# Define the API endpoint for predicting the winner
@app.post("/predict_winner")
async def predict_winner(request: Request):
    # Get the request body
    request_body = await request.json()
    
    # Extract the features from the request body
    features = np.array([
        request_body["car_speed"],
        request_body["car_acceleration"],
        request_body["car_handling"],
        request_body["track_difficulty"],
    ])
    
    # Make a prediction using the trained model
    prediction = model.predict(features)
    
    # Return the prediction as a JSON response
    return JSONResponse(content={"winner": prediction}, media_type="application/json")

# Define the API endpoint for getting the game statistics
@app.get("/game_statistics")
async def get_game_statistics():
    # Load the game statistics from the data loader
    statistics = data_loader.load_game_statistics()
    
    # Return the statistics as a JSON response
    return JSONResponse(content=statistics, media_type="application/json")

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)