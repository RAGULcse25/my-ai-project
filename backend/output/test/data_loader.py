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
    - file_path (str): The path to the CSV file.

    Returns:
    - dataset (pd.DataFrame): The loaded dataset.
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
    - dataset (pd.DataFrame): The dataset to clean.

    Returns:
    - cleaned_dataset (pd.DataFrame): The cleaned dataset.
    """
    try:
        # Check for missing values and fill them with the mean of the respective column
        dataset.fillna(dataset.mean(), inplace=True)

        # Scale the features using StandardScaler
        scaler = StandardScaler()
        dataset[['feature1', 'feature2', 'feature3']] = scaler.fit_transform(dataset[['feature1', 'feature2', 'feature3']])

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
    - dataset (pd.DataFrame): The dataset to split.

    Returns:
    - X_train (pd.DataFrame): The training features.
    - X_test (pd.DataFrame): The testing features.
    - y_train (pd.Series): The training target variable.
    - y_test (pd.Series): The testing target variable.
    """
    try:
        # Split the dataset into features (X) and target variable (y)
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
    file_path = "data.csv"  # Replace with the actual file path
    dataset = load_dataset(file_path)
    cleaned_dataset = clean_dataset(dataset)
    X_train, X_test, y_train, y_test = split_dataset(cleaned_dataset)
    print("Dataset loaded, cleaned, and split successfully.")