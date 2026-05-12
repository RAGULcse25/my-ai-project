# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# Load dataset
def load_dataset(data_loader):
    # Load chess dataset from data loader
    dataset = data_loader.load_chess_dataset()
    return dataset

# Preprocess dataset
def preprocess_dataset(dataset):
    # Convert categorical variables to numerical variables
    dataset['piece'] = dataset['piece'].map({'king': 0, 'queen': 1, 'rook': 2, 'bishop': 3, 'knight': 4, 'pawn': 5})
    dataset['color'] = dataset['color'].map({'white': 0, 'black': 1})
    
    # Define features and target
    X = dataset[['piece', 'color', 'x', 'y']]
    y = dataset['move']
    
    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features using StandardScaler
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test

# Train model
def train_model(X_train, y_train):
    # Initialize and train RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# Evaluate model
def evaluate_model(model, X_test, y_test):
    # Make predictions on test set
    y_pred = model.predict(X_test)
    
    # Evaluate model using accuracy score, classification report, and confusion matrix
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)
    
    return accuracy, report, matrix

# Save model
def save_model(model):
    # Save trained model to file
    import pickle
    with open('chess_model.pkl', 'wb') as f:
        pickle.dump(model, f)

# Main function
def main(data_loader):
    # Load dataset
    dataset = load_dataset(data_loader)
    
    # Preprocess dataset
    X_train, X_test, y_train, y_test = preprocess_dataset(dataset)
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    accuracy, report, matrix = evaluate_model(model, X_test, y_test)
    
    # Save model
    save_model(model)
    
    return model

# Example usage
if __name__ == '__main__':
    from data_loader import DataLoader
    data_loader = DataLoader()
    model = main(data_loader)