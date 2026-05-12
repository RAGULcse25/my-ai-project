# Import necessary libraries
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from model import RacingModel
from data_loader import DataLoader
import uvicorn
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastAPI app
app = FastAPI()

# Enable CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the dataset and train the model
data_loader = DataLoader()
model = RacingModel()
model.train(data_loader.load_data())

# Define the API endpoint for predicting the winner
@app.post("/predict_winner")
async def predict_winner(request: Request):
    try:
        # Get the request data
        data = await request.json()
        
        # Validate the request data
        if not data or "car1" not in data or "car2" not in data:
            raise HTTPException(status_code=400, detail="Invalid request data")
        
        # Predict the winner
        winner = model.predict(data["car1"], data["car2"])
        
        # Return the prediction result
        return JSONResponse(content={"winner": winner}, status_code=200)
    except Exception as e:
        # Log the error and return a 500 error response
        logger.error(f"Error predicting winner: {str(e)}")
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)

# Define the API endpoint for getting the model's performance metrics
@app.get("/model_metrics")
async def get_model_metrics():
    try:
        # Get the model's performance metrics
        metrics = model.get_metrics()
        
        # Return the metrics
        return JSONResponse(content=metrics, status_code=200)
    except Exception as e:
        # Log the error and return a 500 error response
        logger.error(f"Error getting model metrics: {str(e)}")
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)