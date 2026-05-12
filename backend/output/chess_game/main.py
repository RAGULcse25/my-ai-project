# Import necessary libraries
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import sqlite3
from data_loader import load_data
from model import train_model

# Initialize the FastAPI application
app = FastAPI()

# Define the CORS policy
origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request and response models
class MoveRequest(BaseModel):
    board: str
    move: str

class MoveResponse(BaseModel):
    move: str
    score: float

# Load the dataset and train the model
data = load_data()
model = train_model(data)

# Define the API endpoint for making a move
@app.post("/make_move", response_model=MoveResponse)
async def make_move(request: MoveRequest):
    # Get the current board and move from the request
    board = request.board
    move = request.move

    # Make a prediction using the trained model
    prediction = model.predict(np.array([board]))

    # Return the predicted move and score
    return {"move": prediction[0], "score": 1.0}

# Define the API endpoint for getting the current board
@app.get("/get_board")
async def get_board():
    # Connect to the SQLite database
    conn = sqlite3.connect("chess.db")
    cursor = conn.cursor()

    # Retrieve the current board from the database
    cursor.execute("SELECT board FROM games WHERE id = 1")
    board = cursor.fetchone()[0]

    # Return the current board
    return {"board": board}

# Define the API endpoint for resetting the game
@app.post("/reset_game")
async def reset_game():
    # Connect to the SQLite database
    conn = sqlite3.connect("chess.db")
    cursor = conn.cursor()

    # Reset the game by deleting all moves
    cursor.execute("DELETE FROM moves")
    conn.commit()

    # Return a success message
    return {"message": "Game reset successfully"}

# Define a custom exception handler for the application
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Return a JSON response with the error message
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)