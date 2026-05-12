# Import necessary libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import sqlite3
import numpy as np
from model import train_model
from data_loader import load_data

# Initialize the FastAPI application
app = FastAPI()

# Define CORS policy
origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a request body model for API endpoint
class BuildRequest(BaseModel):
    key1: str
    key2: str
    key3: str
    key4: str
    key5: str

# Load the dataset
@app.on_event("startup")
def load_dataset():
    # Load the dataset from SQLite database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dataset")
    rows = cursor.fetchall()
    data = pd.DataFrame(rows)
    # Clean the dataset
    data = load_data(data)
    # Train the ML model
    global model
    model = train_model(data)

# Define the API endpoint for parallel build testing
@app.post("/build")
async def build(request: BuildRequest):
    # Extract the keys from the request body
    keys = [request.key1, request.key2, request.key3, request.key4, request.key5]
    # Make predictions using the trained ML model
    predictions = model.predict(keys)
    # Return the predictions as a JSON response
    return JSONResponse(content={"predictions": predictions.tolist()}, media_type="application/json")

# Define a route for the frontend UI
@app.get("/ui")
async def ui(request: Request):
    # Return the frontend UI as an HTML response
    return {"message": "Parallel Build Tester UI"}

# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)