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
    Clean the dataset by handling missing values and scaling features.
    
    Args:
    dataset (pandas.DataFrame): The dataset to clean.
    
    Returns:
    pandas.DataFrame: The cleaned dataset.
    """
    # Check for missing values and replace with mean or median if necessary
    for column in dataset.columns:
        if dataset[column].isnull().any():
            if dataset[column].dtype == 'object':
                dataset[column] = dataset[column].fillna(dataset[column].mode()[0])
            else:
                dataset[column] = dataset[column].fillna(dataset[column].mean())
    
    # Scale features using StandardScaler
    scaler = StandardScaler()
    dataset[['speed', 'acceleration', 'braking']] = scaler.fit_transform(dataset[['speed', 'acceleration', 'braking']])
    
    return dataset

# Define a function to split the dataset into training and testing sets
def split_dataset(dataset):
    """
    Split the dataset into training and testing sets.
    
    Args:
    dataset (pandas.DataFrame): The dataset to split.
    
    Returns:
    tuple: The training and testing sets.
    """
    # Split the dataset into features (X) and target (y)
    X = dataset.drop('result', axis=1)
    y = dataset['result']
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

# Example usage
if __name__ == "__main__":
    # Load the dataset
    dataset = load_dataset('data.csv')
    
    # Clean the dataset
    cleaned_dataset = clean_dataset(dataset)
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = split_dataset(cleaned_dataset)
    
    # Print the shapes of the training and testing sets
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"y_test shape: {y_test.shape}")