# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Load data from data_loader
from data_loader import load_data

# Load dataset
def load_dataset():
    """Loads the dataset from the data loader"""
    data = load_data()
    return data

# Preprocess data
def preprocess_data(data):
    """Preprocesses the data by scaling and encoding"""
    # Separate features and target
    X = data.drop('lap_time', axis=1)  # features
    y = data['lap_time']  # target
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y

# Train model
def train_model(X_scaled, y):
    """Trains a random forest regressor model"""
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # Initialize and train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions and evaluate model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Model MSE: {mse}")
    
    return model

# Main function to train the model
def main():
    data = load_dataset()
    X_scaled, y = preprocess_data(data)
    model = train_model(X_scaled, y)
    return model

if __name__ == "__main__":
    main()