# Chess Game Project
======================
## Overview
The Chess Game Project is a web-based chess game with an AI-powered opponent. The project utilizes Python as the primary language, FastAPI as the framework, and scikit-learn for machine learning tasks.

## Project Structure
The project consists of the following files:
- `main.py`: The main application file
- `model.py`: The machine learning model file
- `data_loader.py`: The data loading file
- `requirements.txt`: The dependencies file
- `README.md`: This documentation file

## Getting Started
To get started with the project, follow these steps:
1. Clone the repository using `git clone`
2. Install the dependencies using `pip install -r requirements.txt`
3. Run the application using `uvicorn main:app --host 0.0.0.0 --port 8000`

## Dependencies
The project requires the following dependencies:
- fastapi
- uvicorn
- scikit-learn
- pandas
- numpy
- streamlit

## API Endpoints
The application exposes the following API endpoints:
- `/make_move`: Makes a move on the chess board
- `/get_board`: Returns the current state of the chess board
- `/reset_board`: Resets the chess board to its initial state

## Machine Learning Model
The machine learning model is trained using the scikit-learn library and utilizes a decision tree classifier to predict the best move based on the current state of the board.

## Data Loading
The data loading file `data_loader.py` loads the chess dataset from a CSV file and preprocesses it for training the machine learning model.

## Frontend UI
The frontend UI is built using Streamlit and provides a simple and intuitive interface for playing the chess game.

## Contributing
To contribute to the project, please fork the repository and submit a pull request with your changes. Ensure that your code is well-documented and follows the project's coding standards.

## License
The project is licensed under the MIT License. See the LICENSE file for more information.