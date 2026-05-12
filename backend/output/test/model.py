# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# Load dataset from data_loader module
from data_loader import load_dataset

# Define a function to train the model
def train_model():
    # Load the dataset
    dataset = load_dataset()
    
    # Split the dataset into features (X) and target (y)
    X = dataset.drop('target', axis=1)  # Assuming 'target' is the target column
    y = dataset['target']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and fit the scaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Initialize the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Train the model
    model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_scaled)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)
    
    # Print the evaluation metrics
    print(f"Model Accuracy: {accuracy:.3f}")
    print("Classification Report:\n", report)
    print("Confusion Matrix:\n", matrix)
    
    # Return the trained model and the scaler
    return model, scaler

# Define a function to make predictions
def make_prediction(model, scaler, data):
    # Scale the data
    scaled_data = scaler.transform(data)
    
    # Make predictions
    predictions = model.predict(scaled_data)
    
    # Return the predictions
    return predictions