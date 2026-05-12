# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# Load data from data_loader.py
from data_loader import load_data

# Define a function to train the model
def train_model(data):
    # Split data into features and target
    X = data.drop('target', axis=1)  # Assuming 'target' is the target variable
    y = data['target']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and fit the scaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test_scaled)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)

    return model, accuracy, report, matrix

# Define a function to make predictions
def make_prediction(model, data):
    # Scale the data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    # Make predictions
    predictions = model.predict(data_scaled)

    return predictions

# Example usage
if __name__ == "__main__":
    # Load the data
    data = load_data()

    # Train the model
    model, accuracy, report, matrix = train_model(data)

    # Print the results
    print("Model Accuracy:", accuracy)
    print("Classification Report:\n", report)
    print("Confusion Matrix:\n", matrix)

    # Make predictions
    predictions = make_prediction(model, data)
    print("Predictions:", predictions)