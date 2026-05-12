# Chess Game Project
======================
## Overview
This project is a web-based chess game with an AI opponent. The game is built using Python, with a FastAPI backend and a Streamlit frontend. The AI opponent is trained using a machine learning model implemented with scikit-learn and pandas.

## Project Structure
The project consists of the following files:
* `main.py`: The main application file, responsible for running the FastAPI server.
* `model.py`: The machine learning model file, responsible for training and predicting moves.
* `data_loader.py`: The data loading file, responsible for loading and cleaning the dataset.
* `requirements.txt`: The requirements file, listing all dependencies required to run the project.
* `README.md`: This file, providing an overview of the project and its components.

## Getting Started
To get started with the project, follow these steps:
1. Clone the repository using `git clone`.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the application using `uvicorn main:app --host 0.0.0.0 --port 8000`.
4. Open a web browser and navigate to `http://localhost:8000` to play the game.

## Dependencies
The project requires the following dependencies:
* `fastapi`
* `streamlit`
* `scikit-learn`
* `pandas`
* `numpy`
* `sqlite3`

## Dataset
The dataset used to train the machine learning model consists of chess games in PGN format. The dataset is loaded and cleaned using the `data_loader.py` file.

## Machine Learning Model
The machine learning model is implemented using scikit-learn and pandas. The model is trained on the dataset and used to predict moves for the AI opponent.

## API Endpoints
The FastAPI server provides the following API endpoints:
* `/move`: Predicts the next move for the AI opponent.
* `/game`: Starts a new game.
* `/board`: Returns the current state of the board.

## Frontend
The frontend is built using Streamlit and provides a user-friendly interface for playing the game.

## Contributing
Contributions to the project are welcome. To contribute, please fork the repository and submit a pull request with your changes.

## License
The project is licensed under the MIT License.