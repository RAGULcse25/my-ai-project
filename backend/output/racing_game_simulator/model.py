# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Load data from data_loader.py
from data_loader import load_data

# Define a function to prepare data for training
def prepare_data(data):
    # Convert categorical variables to numerical variables
    data = pd.get_dummies(data, columns=['car_type', 'track_type'])
    
    # Define features and target
    X = data.drop('lap_time', axis=1)
    y = data['lap_time']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features using StandardScaler
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test

# Define a function to train the model
def train_model(X_train, y_train):
    # Initialize and train a RandomForestRegressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model

# Define a function to evaluate the model
def evaluate_model(model, X_test, y_test):
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Calculate the mean squared error
    mse = mean_squared_error(y_test, y_pred)
    
    return mse

# Define a function to save the model
def save_model(model):
    # Import necessary library
    import pickle
    
    # Save the model to a file
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

# Load data
data = load_data()

# Prepare data
X_train, X_test, y_train, y_test = prepare_data(data)

# Train model
model = train_model(X_train, y_train)

# Evaluate model
mse = evaluate_model(model, X_test, y_test)
print(f'Mean Squared Error: {mse}')

# Save model
save_model(model)