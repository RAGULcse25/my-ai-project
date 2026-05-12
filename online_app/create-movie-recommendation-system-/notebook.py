# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import NMF

# %%
# Generate synthetic dataset
np.random.seed(0)
n_users = 100
n_movies = 100
n_ratings = 500
user_ids = np.random.randint(0, n_users, n_ratings)
movie_ids = np.random.randint(0, n_movies, n_ratings)
ratings = np.random.randint(1, 6, n_ratings)
df = pd.DataFrame({
    'user_id': user_ids,
    'movie_id': movie_ids,
    'rating': ratings
})
print(df.shape, df.head())

# %%
# EDA
plt.figure(figsize=(10, 6))
sns.countplot(x='movie_id', data=df)
plt.title('Movie Ratings Distribution')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(x='user_id', data=df)
plt.title('User Ratings Distribution')
plt.show()

# %%
# Preprocessing
user_item_matrix = pd.pivot_table(df, values='rating', index='user_id', columns='movie_id')
user_item_matrix.fillna(0, inplace=True)
print(user_item_matrix.shape, user_item_matrix.head())

# %%
# Model Training
X_train, X_test = train_test_split(user_item_matrix, test_size=0.2, random_state=42)
nmf = NMF(n_components=10, random_state=42)
nmf.fit(X_train)

# %%
# Evaluation
X_pred = nmf.transform(X_test)
X_pred = nmf.inverse_transform(X_pred)
mse = mean_squared_error(X_test, X_pred)
print(f'MSE: {mse}')

# %%
# Recommendation
def recommend(user_id, num_recs=5):
    user_idx = np.where(user_item_matrix.index == user_id)[0][0]
    user_vec = nmf.transform(user_item_matrix)[user_idx]
    scores = np.dot(nmf.components_, user_vec)
    top_scores = np.argsort(-scores)[:num_recs]
    return top_scores

user_id = 10
recs = recommend(user_id)
print(f'Recommended movies for user {user_id}: {recs}')

# %%
# Nearest Neighbors
nn = NearestNeighbors(n_neighbors=10, algorithm='brute', metric='cosine')
nn.fit(nmf.transform(user_item_matrix))

# %%
# Similar Users
def similar_users(user_id, num_sim=5):
    user_idx = np.where(user_item_matrix.index == user_id)[0][0]
    user_vec = nmf.transform(user_item_matrix)[user_idx]
    distances, indices = nn.kneighbors([user_vec])
    return indices[0]

user_id = 10
sim_users = similar_users(user_id)
print(f'Similar users to user {user_id}: {sim_users}')

# %%
# Hybrid Recommendation
def hybrid_recommend(user_id, num_recs=5):
    recs = recommend(user_id)
    sim_users = similar_users(user_id)
    sim_user_recs = []
    for sim_user in sim_users:
        sim_user_recs.extend(recommend(sim_user))
    sim_user_recs = np.unique(sim_user_recs)
    hybrid_recs = np.concatenate((recs, sim_user_recs))
    hybrid_recs = np.unique(hybrid_recs)[:num_recs]
    return hybrid_recs

user_id = 10
hybrid_recs = hybrid_recommend(user_id)
print(f'Hybrid recommended movies for user {user_id}: {hybrid_recs}')