# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Define a function to load the dataset
def load_dataset(file_path):
    """
    Loads the chess dataset from a CSV file.
    
    Args:
    file_path (str): The path to the CSV file.
    
    Returns:
    pandas.DataFrame: The loaded dataset.
    """
    try:
        # Attempt to load the dataset from the specified file path
        dataset = pd.read_csv(file_path)
        return dataset
    except FileNotFoundError:
        # Handle the case where the file is not found
        print("The file was not found. Please check the file path.")
        return None
    except pd.errors.EmptyDataError:
        # Handle the case where the file is empty
        print("The file is empty. Please check the file contents.")
        return None

# Define a function to clean the dataset
def clean_dataset(dataset):
    """
    Cleans the chess dataset by handling missing values and encoding categorical variables.
    
    Args:
    dataset (pandas.DataFrame): The dataset to be cleaned.
    
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
    Splits the chess dataset into training and testing sets.
    
    Args:
    dataset (pandas.DataFrame): The dataset to be split.
    
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
    Scales the chess dataset using StandardScaler.
    
    Args:
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
    cleaned_dataset = clean_dataset(dataset)
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = split_dataset(cleaned_dataset)
    
    # Scale the dataset
    X_train_scaled, X_test_scaled = scale_dataset(X_train, X_test)