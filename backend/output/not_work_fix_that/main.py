# Import required libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from model import NotWorkFixThatModel
from data_loader import DataLoader

# Initialize the FastAPI application
app = FastAPI()

# Define CORS policy
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

# Define a Pydantic model for the request body
class NotWorkFixThatRequest(BaseModel):
    text: str

# Load the dataset and train the model
data_loader = DataLoader()
model = NotWorkFixThatModel()
model.train(data_loader.load_data())

# Define the API endpoint
@app.post("/predict")
async def predict(request: NotWorkFixThatRequest):
    # Use the trained model to make a prediction
    prediction = model.predict(request.text)
    return JSONResponse(content={"prediction": prediction}, media_type="application/json")

# Define a route for the frontend to fetch data
@app.get("/data")
async def get_data():
    # Load the dataset
    data = data_loader.load_data()
    return JSONResponse(content=data.to_dict(orient="records"), media_type="application/json")

# Define a route for the frontend to send feedback
@app.post("/feedback")
async def send_feedback(request: Request):
    # Get the feedback from the request body
    feedback = await request.json()
    # Save the feedback to the database
    # For this example, we'll just print the feedback
    print(feedback)
    return JSONResponse(content={"message": "Feedback received"}, media_type="application/json")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)