# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import numpy as np
import pickle

# Load dataset
def load_dataset(file_path):
    # Load chess dataset from CSV file
    dataset = pd.read_csv(file_path)
    return dataset

# Preprocess dataset
def preprocess_dataset(dataset):
    # Define features (X) and target (y)
    X = dataset.drop(['result'], axis=1)  # features
    y = dataset['result']  # target

    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features using StandardScaler
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test

# Train ML model
def train_model(X_train, y_train):
    # Initialize and train RandomForestClassifier model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# Evaluate ML model
def evaluate_model(model, X_test, y_test):
    # Make predictions on test set
    y_pred = model.predict(X_test)

    # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)

    return accuracy, report, matrix

# Save ML model to file
def save_model(model, file_path):
    # Use pickle to save model to file
    with open(file_path, 'wb') as file:
        pickle.dump(model, file)

# Load ML model from file
def load_model(file_path):
    # Use pickle to load model from file
    with open(file_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Main function to train and evaluate ML model
def main():
    # Load dataset
    dataset = load_dataset('data/chess_dataset.csv')

    # Preprocess dataset
    X_train, X_test, y_train, y_test = preprocess_dataset(dataset)

    # Train ML model
    model = train_model(X_train, y_train)

    # Evaluate ML model
    accuracy, report, matrix = evaluate_model(model, X_test, y_test)

    # Print evaluation metrics
    print(f'Accuracy: {accuracy:.3f}')
    print('Classification Report:')
    print(report)
    print('Confusion Matrix:')
    print(matrix)

    # Save ML model to file
    save_model(model, 'models/chess_model.pkl')

if __name__ == '__main__':
    main()