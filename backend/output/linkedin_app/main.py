# Import necessary libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import pandas as pd
from model import LinkedInModel
from data_loader import load_data

# Define the FastAPI application
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

# Define a Pydantic model for user data
class UserData(BaseModel):
    user_id: int
    name: str
    email: str
    connections: list

# Load the dataset
data = load_data()

# Train the ML model
model = LinkedInModel()
model.train(data)

# Define API endpoints
@app.get("/users/")
async def get_users():
    # Return a list of all users
    users = data["users"].to_dict(orient="records")
    return JSONResponse(content=users, media_type="application/json")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Return a specific user by ID
    user = data["users"].loc[data["users"]["user_id"] == user_id].to_dict(orient="records")
    if user:
        return JSONResponse(content=user[0], media_type="application/json")
    else:
        return JSONResponse(content={"error": "User not found"}, media_type="application/json", status_code=404)

@app.post("/users/")
async def create_user(user: UserData):
    # Create a new user
    new_user = pd.DataFrame([user.dict()])
    data["users"] = pd.concat([data["users"], new_user], ignore_index=True)
    return JSONResponse(content=new_user.to_dict(orient="records")[0], media_type="application/json", status_code=201)

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserData):
    # Update an existing user
    user_index = data["users"].loc[data["users"]["user_id"] == user_id].index
    if user_index.empty:
        return JSONResponse(content={"error": "User not found"}, media_type="application/json", status_code=404)
    data["users"].at[user_index[0], "name"] = user.name
    data["users"].at[user_index[0], "email"] = user.email
    data["users"].at[user_index[0], "connections"] = user.connections
    return JSONResponse(content=data["users"].loc[user_index[0]].to_dict(), media_type="application/json")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    # Delete a user by ID
    user_index = data["users"].loc[data["users"]["user_id"] == user_id].index
    if user_index.empty:
        return JSONResponse(content={"error": "User not found"}, media_type="application/json", status_code=404)
    data["users"].drop(user_index, inplace=True)
    return JSONResponse(content={"message": "User deleted successfully"}, media_type="application/json", status_code=200)

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)