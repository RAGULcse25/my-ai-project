# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# Define a class for the machine learning model
class MachineLearningModel:
    def __init__(self):
        # Initialize the model and scaler
        self.model = RandomForestClassifier(n_estimators=100)
        self.scaler = StandardScaler()

    # Method to load and preprocess the data
    def load_and_preprocess_data(self, data):
        # Drop any rows with missing values
        data.dropna(inplace=True)
        
        # Split the data into features and target
        X = data.drop('target', axis=1)
        y = data['target']
        
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        return X_train, X_test, y_train, y_test

    # Method to train the model
    def train_model(self, X_train, y_train):
        # Train the model on the training data
        self.model.fit(X_train, y_train)

    # Method to make predictions
    def make_predictions(self, X_test):
        # Make predictions on the testing data
        y_pred = self.model.predict(X_test)
        
        return y_pred

    # Method to evaluate the model
    def evaluate_model(self, y_test, y_pred):
        # Calculate the accuracy of the model
        accuracy = accuracy_score(y_test, y_pred)
        
        # Print the classification report and confusion matrix
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        return accuracy

# Example usage
if __name__ == "__main__":
    # Load the data
    data = pd.read_csv('data.csv')
    
    # Create an instance of the machine learning model
    ml_model = MachineLearningModel()
    
    # Load and preprocess the data
    X_train, X_test, y_train, y_test = ml_model.load_and_preprocess_data(data)
    
    # Train the model
    ml_model.train_model(X_train, y_train)
    
    # Make predictions
    y_pred = ml_model.make_predictions(X_test)
    
    # Evaluate the model
    accuracy = ml_model.evaluate_model(y_test, y_pred)
    
    print("Model Accuracy:", accuracy)