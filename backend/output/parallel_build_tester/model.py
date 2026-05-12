# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
def load_dataset(data_loader):
    # Load data from data loader
    data = data_loader.load_data()
    return data

# Preprocess dataset
def preprocess_dataset(data):
    # Convert categorical variables to numerical variables
    data = pd.get_dummies(data, drop_first=True)
    # Split dataset into features and target variable
    X = data.drop('target', axis=1)
    y = data['target']
    return X, y

# Train model
def train_model(X, y):
    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Initialize and train random forest classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    # Make predictions on test set
    y_pred = model.predict(X_test)
    # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)
    return model, accuracy, report, matrix

# Save model
def save_model(model):
    # Import necessary library
    import pickle
    # Save model to file
    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)

# Load model
def load_model():
    # Import necessary library
    import pickle
    # Load model from file
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Main function
def main(data_loader):
    # Load dataset
    data = load_dataset(data_loader)
    # Preprocess dataset
    X, y = preprocess_dataset(data)
    # Train model
    model, accuracy, report, matrix = train_model(X, y)
    # Print model performance
    print(f'Accuracy: {accuracy:.3f}')
    print('Classification Report:')
    print(report)
    print('Confusion Matrix:')
    print(matrix)
    # Save model
    save_model(model)
    return model