# Import necessary libraries
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from model import ChessModel
from data_loader import load_dataset

# Initialize the FastAPI application
app = FastAPI()

# Define CORS policy
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a request body model for the API endpoint
class MoveRequest(BaseModel):
    board_state: str
    move: str

# Load the dataset and train the model
dataset = load_dataset()
model = ChessModel()
model.train(dataset)

# Define the API endpoint for making a move
@app.post("/make_move")
async def make_move(request: MoveRequest):
    # Get the current board state and the move from the request body
    board_state = request.board_state
    move = request.move
    
    # Use the trained model to predict the best response
    response = model.predict(board_state, move)
    
    # Return the response as a JSON object
    return JSONResponse(content={"response": response}, media_type="application/json")

# Define the API endpoint for getting the current board state
@app.get("/get_board_state")
async def get_board_state():
    # Return the current board state as a JSON object
    return JSONResponse(content={"board_state": model.get_board_state()}, media_type="application/json")

# Define a route for the root of the API
@app.get("/")
async def root():
    # Return a welcome message
    return {"message": "Welcome to the Chess Game API"}

# Run the application if this script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)