# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Define a function to load the dataset
def load_dataset(file_path):
    """
    Load the dataset from a CSV file.
    
    Args:
    file_path (str): The path to the CSV file.
    
    Returns:
    pd.DataFrame: The loaded dataset.
    """
    try:
        # Attempt to load the dataset
        dataset = pd.read_csv(file_path)
        return dataset
    except Exception as e:
        # Handle any exceptions that occur during loading
        print(f"Error loading dataset: {e}")
        return None

# Define a function to clean the dataset
def clean_dataset(dataset):
    """
    Clean the dataset by handling missing values and encoding categorical variables.
    
    Args:
    dataset (pd.DataFrame): The dataset to be cleaned.
    
    Returns:
    pd.DataFrame: The cleaned dataset.
    """
    # Check for missing values
    if dataset.isnull().values.any():
        # Handle missing values by replacing with mean or mode
        dataset.fillna(dataset.mean(), inplace=True)
    
    # Encode categorical variables
    categorical_cols = dataset.select_dtypes(include=['object']).columns
    dataset[categorical_cols] = dataset[categorical_cols].apply(lambda x: pd.factorize(x)[0])
    
    return dataset

# Define a function to split the dataset into training and testing sets
def split_dataset(dataset, test_size=0.2):
    """
    Split the dataset into training and testing sets.
    
    Args:
    dataset (pd.DataFrame): The dataset to be split.
    test_size (float): The proportion of the dataset to be used for testing.
    
    Returns:
    tuple: The training and testing sets.
    """
    # Split the dataset into features and target
    X = dataset.drop('target', axis=1)  # Assuming 'target' is the target variable
    y = dataset['target']
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    return X_train, X_test, y_train, y_test

# Define a function to scale the dataset
def scale_dataset(X_train, X_test):
    """
    Scale the dataset using StandardScaler.
    
    Args:
    X_train (pd.DataFrame): The training set.
    X_test (pd.DataFrame): The testing set.
    
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
    dataset = load_dataset('data.csv')
    
    # Clean the dataset
    cleaned_dataset = clean_dataset(dataset)
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = split_dataset(cleaned_dataset)
    
    # Scale the dataset
    X_train_scaled, X_test_scaled = scale_dataset(X_train, X_test)