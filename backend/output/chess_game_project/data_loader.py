# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Define a function to load the dataset
def load_dataset(file_path):
    """
    Load the chess dataset from a CSV file.
    
    Parameters:
    file_path (str): The path to the CSV file.
    
    Returns:
    pandas.DataFrame: The loaded dataset.
    """
    try:
        # Attempt to load the dataset from the CSV file
        dataset = pd.read_csv(file_path)
        return dataset
    except Exception as e:
        # Handle any exceptions that occur during loading
        print(f"Error loading dataset: {e}")
        return None

# Define a function to clean the dataset
def clean_dataset(dataset):
    """
    Clean the chess dataset by handling missing values and encoding categorical variables.
    
    Parameters:
    dataset (pandas.DataFrame): The dataset to clean.
    
    Returns:
    pandas.DataFrame: The cleaned dataset.
    """
    # Check for missing values
    if dataset.isnull().values.any():
        # Handle missing values by replacing them with the mean or median
        dataset.fillna(dataset.mean(), inplace=True)
    
    # Encode categorical variables
    categorical_cols = dataset.select_dtypes(include=['object']).columns
    dataset[categorical_cols] = dataset[categorical_cols].apply(lambda x: pd.factorize(x)[0])
    
    return dataset

# Define a function to split the dataset into training and testing sets
def split_dataset(dataset):
    """
    Split the chess dataset into training and testing sets.
    
    Parameters:
    dataset (pandas.DataFrame): The dataset to split.
    
    Returns:
    tuple: The training and testing sets.
    """
    # Split the dataset into features (X) and target (y)
    X = dataset.drop('result', axis=1)  # Assuming 'result' is the target column
    y = dataset['result']
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

# Define a function to scale the dataset
def scale_dataset(X_train, X_test):
    """
    Scale the chess dataset using StandardScaler.
    
    Parameters:
    X_train (pandas.DataFrame): The training set.
    X_test (pandas.DataFrame): The testing set.
    
    Returns:
    tuple: The scaled training and testing sets.
    """
    # Create a StandardScaler object
    scaler = StandardScaler()
    
    # Fit the scaler to the training set and transform both sets
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled

# Example usage
if __name__ == "__main__":
    # Load the dataset
    dataset = load_dataset('chess_dataset.csv')
    
    # Clean the dataset
    dataset = clean_dataset(dataset)
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = split_dataset(dataset)
    
    # Scale the dataset
    X_train_scaled, X_test_scaled = scale_dataset(X_train, X_test)