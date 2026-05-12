# %% [markdown]
# # Create House Price Prediction Ml Project With Sklearn
# ## Problem Statement
# The goal of this project is to predict house prices based on various features such as number of bedrooms, number of bathrooms, square footage, and location.

# %% imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# %% [markdown]
# ## 1. Data Loading and Exploration
# We will generate a synthetic dataset for this example.

# %% data loading
# Generate synthetic dataset
np.random.seed(0)
df = pd.DataFrame({
    'bedrooms': np.random.randint(1, 6, 1000),
    'bathrooms': np.random.randint(1, 4, 1000),
    'sqft': np.random.randint(500, 5000, 1000),
    'location': np.random.choice(['urban', 'suburban', 'rural'], 1000),
    'price': np.random.randint(100000, 1000000, 1000)
})
print(df.shape, df.head())

# %% [markdown]
# ## 2. EDA
# Perform exploratory data analysis to understand the distribution of the data.

# %% eda
plt.figure(figsize=(10, 6))
sns.scatterplot(x='sqft', y='price', data=df)
plt.title('Scatterplot of Square Footage vs Price')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='location', y='price', data=df)
plt.title('Boxplot of Location vs Price')
plt.show()

# %% [markdown]
# ## 3. Preprocessing
# Convert categorical variables into numerical variables and scale the data.

# %% preprocessing
df['location'] = df['location'].map({'urban': 0, 'suburban': 1, 'rural': 2})
X = df[['bedrooms', 'bathrooms', 'sqft', 'location']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# %% [markdown]
# ## 4. Model Training
# Train a linear regression model and a random forest regressor model.

# %% training
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# %% [markdown]
# ## 5. Evaluation
# Evaluate the performance of the models using mean squared error and R-squared score.

# %% evaluation
y_pred_lr = lr_model.predict(X_test_scaled)
y_pred_rf = rf_model.predict(X_test_scaled)

print('Linear Regression Model:')
print('Mean Squared Error:', mean_squared_error(y_test, y_pred_lr))
print('R-squared Score:', r2_score(y_test, y_pred_lr))

print('Random Forest Regressor Model:')
print('Mean Squared Error:', mean_squared_error(y_test, y_pred_rf))
print('R-squared Score:', r2_score(y_test, y_pred_rf))