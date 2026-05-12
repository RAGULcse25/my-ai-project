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
    dataset (pandas.DataFrame): The dataset to clean.
    
    Returns:
    pandas.DataFrame: The cleaned dataset.
    """
    # Check for missing values
    if dataset.isnull().values.any():
        # Replace missing values with the mean for numerical columns
        dataset[numerical_columns(dataset)] = dataset[numerical_columns(dataset)].fillna(dataset[numerical_columns(dataset)].mean())
        # Replace missing values with the mode for categorical columns
        dataset[categorical_columns(dataset)] = dataset[categorical_columns(dataset)].fillna(dataset[categorical_columns(dataset)].mode().iloc[0])
    
    # Encode categorical variables
    categorical_cols = categorical_columns(dataset)
    dataset[categorical_cols] = dataset[categorical_cols].apply(lambda x: pd.factorize(x)[0])
    
    return dataset

# Define a function to split the dataset into training and testing sets
def split_dataset(dataset, test_size=0.2, random_state=42):
    """
    Split the dataset into training and testing sets.
    
    Args:
    dataset (pandas.DataFrame): The dataset to split.
    test_size (float, optional): The proportion of the dataset to use for testing. Defaults to 0.2.
    random_state (int, optional): The random seed to use for splitting. Defaults to 42.
    
    Returns:
    tuple: The training and testing sets.
    """
    # Split the dataset into features and target
    X = dataset.drop('target', axis=1)  # Assuming 'target' is the target variable
    y = dataset['target']
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    return X_train, X_test, y_train, y_test

# Define a function to scale the dataset
def scale_dataset(X_train, X_test):
    """
    Scale the dataset using StandardScaler.
    
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

# Define helper functions to get numerical and categorical columns
def numerical_columns(dataset):
    """
    Get the numerical columns in the dataset.
    
    Args:
    dataset (pandas.DataFrame): The dataset.
    
    Returns:
    list: The numerical columns.
    """
    return dataset.select_dtypes(include=['int64', 'float64']).columns

def categorical_columns(dataset):
    """
    Get the categorical columns in the dataset.
    
    Args:
    dataset (pandas.DataFrame): The dataset.
    
    Returns:
    list: The categorical columns.
    """
    return dataset.select_dtypes(include=['object']).columns