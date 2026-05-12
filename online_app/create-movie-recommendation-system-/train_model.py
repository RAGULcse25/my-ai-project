```python
import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from joblib import dump
from rich.console import Console
from rich.table import Table
from rich.progress import track

# Synthetic dataset generation
def generate_movie_data(num_users=500, num_movies=100):
    np.random.seed(42)
    user_ids = np.arange(num_users)
    movie_ids = np.arange(num_movies)
    
    # Generate user-movie matrix
    ratings = np.random.randint(1, 6, size=(num_users, num_movies))
    
    # Add some patterns
    for i in track(range(num_users)):
        favorite_genre = np.random.choice(['action', 'comedy', 'drama'])
        if favorite_genre == 'action':
            ratings[i, :30] += np.random.randint(0, 2, size=30)
        elif favorite_genre == 'comedy':
            ratings[i, 30:60] += np.random.randint(0, 2, size=30)
        else:
            ratings[i, 60:] += np.random.randint(0, 2, size=40)
    
    # Create DataFrame
    data = pd.DataFrame(ratings, 
                        index=[f'user_{i}' for i in user_ids],
                        columns=[f'movie_{i}' for i in movie_ids])
    
    return data

# Model training
def train_collaborative_filtering(data):
    # Split data
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    
    # Matrix Factorization
    model = NMF(n_components=20, init='random', random_state=42)
    W = model.fit_transform(train_data)
    H = model.components_
    
    # Predictions
    predictions = np.dot(W, H)
    
    # Evaluation
    rmse = np.sqrt(mean_squared_error(test_data.values[test_data.values.nonzero()], 
                                    predictions[test_data.values.nonzero()]))
    
    # Save model
    dump(model, 'model.pkl')
    
    return model, rmse

# Main execution
if __name__ == "__main__":
    console = Console()
    
    # Generate data
    console.print("[bold cyan]Generating synthetic movie ratings data...")
    data = generate_movie_data()
    
    # Train model
    console.print("[bold cyan]Training collaborative filtering model...")
    model, rmse = train_collaborative_filtering(data)
    
    # Display results
    table = Table(title="Model Performance")
    table.add_column("Metric", justify="right")
    table.add_column("Value", justify="left")
    table.add_row("RMSE", f"{rmse:.4f}")
    table.add_row("Components", "20")
    table.add_row("Users", "500")
    table.add_row("Movies", "100")
    
    console.print(table)
    console.print("[bold green]Model saved as model.pkl")
```

=