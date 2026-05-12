# === AGENT: House Price Prediction ===
# === FILE: main.py ===
# === TOKENS: 500 ===
# === DEPENDS_ON: numpy, pandas, sklearn ===

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# 1. Generate/load synthetic dataset
np.random.seed(0)
data = {
    'bedrooms': np.random.randint(1, 6, 100),
    'bathrooms': np.random.randint(1, 4, 100),
    'sqft': np.random.randint(500, 5000, 100),
    'location': np.random.choice(['urban', 'suburban', 'rural'], 100),
    'price': np.random.randint(100000, 1000000, 100)
}
df = pd.DataFrame(data)

# 2. EDA
print("Shapes:", df.shape)
print("Dtypes:\n", df.dtypes)
print("Describe:\n", df.describe())
print("Correlations:\n", df.corr())

# 3. Data preprocessing
numeric_features = ['bedrooms', 'bathrooms', 'sqft']
categorical_features = ['location']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

# 4. Feature engineering
# No additional features created for this example

# 5. Train/test split
X = df.drop('price', axis=1)
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Model training
model = Pipeline(steps=[('preprocessor', preprocessor),
                      ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

model.fit(X_train, y_train)

# 7. Evaluation
y_pred = model.predict(X_test)
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R²:", r2_score(y_test, y_pred))

# 8. Prediction function
def predict(input_dict):
    input_df = pd.DataFrame([input_dict])
    result = model.predict(input_df)
    return result[0]

# 9. Save model with joblib
joblib.dump(model, 'house_price_model.joblib')

# Example usage:
input_dict = {'bedrooms': 3, 'bathrooms': 2, 'sqft': 1500, 'location': 'urban'}
print(predict(input_dict))

# === END ===