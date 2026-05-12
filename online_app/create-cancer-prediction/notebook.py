# %% imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

# %% data loading
np.random.seed(0)
df = pd.DataFrame({
    'mean_radius': np.random.uniform(10, 20, 100),
    'mean_texture': np.random.uniform(10, 20, 100),
    'mean_perimeter': np.random.uniform(50, 100, 100),
    'mean_area': np.random.uniform(500, 1000, 100),
    'mean_smoothness': np.random.uniform(0.05, 0.15, 100),
    'mean_compactness': np.random.uniform(0.05, 0.15, 100),
    'mean_concavity': np.random.uniform(0.05, 0.15, 100),
    'mean_concave_points': np.random.uniform(0.05, 0.15, 100),
    'mean_symmetry': np.random.uniform(0.1, 0.3, 100),
    'mean_fractal_dimension': np.random.uniform(0.05, 0.15, 100),
    'cancer_score': np.random.uniform(0, 1, 100)
})
print(df.shape, df.head())

# %% eda
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# %% preprocessing
X = df.drop('cancer_score', axis=1)
y = df['cancer_score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# %% training
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
rf_model = RandomForestRegressor()
rf_model.fit(X_train, y_train)
svm_model = SVR()
svm_model.fit(X_train, y_train)

# %% evaluation
lr_pred = lr_model.predict(X_test)
rf_pred = rf_model.predict(X_test)
svm_pred = svm_model.predict(X_test)
print('Linear Regression MSE: ', mean_squared_error(y_test, lr_pred))
print('Random Forest Regressor MSE: ', mean_squared_error(y_test, rf_pred))
print('Support Vector Regressor MSE: ', mean_squared_error(y_test, svm_pred))
print('Linear Regression R2 Score: ', r2_score(y_test, lr_pred))
print('Random Forest Regressor R2 Score: ', r2_score(y_test, rf_pred))
print('Support Vector Regressor R2 Score: ', r2_score(y_test, svm_pred))