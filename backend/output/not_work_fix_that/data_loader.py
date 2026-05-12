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
    Clean the dataset by handling missing values and scaling features.
    
    Args:
    dataset (pd.DataFrame): The dataset to clean.
    
    Returns:
    pd.DataFrame: The cleaned dataset.
    """
    try:
        # Check for missing values
        if dataset.isnull().values.any():
            # Handle missing values by replacing with mean or median
            dataset.fillna(dataset.mean(), inplace=True)
        
        # Scale features using StandardScaler
        scaler = StandardScaler()
        dataset[['feature1', 'feature2']] = scaler.fit_transform(dataset[['feature1', 'feature2']])
        
        return dataset
    except Exception as e:
        # Handle any exceptions that occur during cleaning
        print(f"Error cleaning dataset: {e}")
        return None

# Define a function to split the dataset into training and testing sets
def split_dataset(dataset):
    """
    Split the dataset into training and testing sets.
    
    Args:
    dataset (pd.DataFrame): The dataset to split.
    
    Returns:
    tuple: The training and testing sets.
    """
    try:
        # Split the dataset into features (X) and target (y)
        X = dataset.drop('target', axis=1)
        y = dataset['target']
        
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        return X_train, X_test, y_train, y_test
    except Exception as e:
        # Handle any exceptions that occur during splitting
        print(f"Error splitting dataset: {e}")
        return None

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