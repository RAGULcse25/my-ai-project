# Parallel Build Tester Project
=====================================

## Table of Contents
-----------------

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Getting Started](#getting-started)
4. [Tasks](#tasks)
5. [Tech Stack](#tech-stack)
6. [Requirements](#requirements)
7. [API Endpoints](#api-endpoints)
8. [Frontend UI](#frontend-ui)
9. [Documentation](#documentation)

## Introduction
---------------

The Parallel Build Tester project is designed to test parallel build with 5 keys using Python, FastAPI, scikit-learn, SQLite, and Streamlit.

## Project Structure
--------------------

The project consists of the following files:
- `main.py`: The main application file
- `model.py`: The machine learning model file
- `data_loader.py`: The data loading file
- `requirements.txt`: The dependencies file
- `README.md`: This documentation file

## Getting Started
------------------

To get started with the project, follow these steps:
1. Clone the repository
2. Install the dependencies using `pip install -r requirements.txt`
3. Run the application using `streamlit run main.py`

## Tasks
--------

The project consists of the following tasks:
1. **Task 1: Load and clean dataset**: Load the dataset and clean it for training
2. **Task 2: Train ML model**: Train a machine learning model using the cleaned dataset
3. **Task 3: Build API endpoint**: Build an API endpoint to serve the trained model
4. **Task 4: Create frontend UI**: Create a frontend UI using Streamlit to interact with the API
5. **Task 5: Write documentation**: Write documentation for the project

## Tech Stack
-------------

The project uses the following tech stack:
- **Language**: Python
- **Framework**: FastAPI
- **ML Library**: scikit-learn
- **Database**: SQLite
- **Frontend**: Streamlit

## Requirements
------------

The project requires the following dependencies:
- fastapi
- scikit-learn
- pandas
- numpy
- streamlit
- sqlite3

## API Endpoints
----------------

The project has the following API endpoints:
- **/train**: Train the machine learning model
- **/predict**: Make predictions using the trained model

## Frontend UI
--------------

The project has a frontend UI built using Streamlit. The UI allows users to interact with the API and view the results.

## Documentation
--------------

This documentation provides an overview of the project, its structure, and its tasks. It also provides information on how to get started with the project and how to use the API endpoints.