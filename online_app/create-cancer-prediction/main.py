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
    'age': np.random.randint(20, 80, 100),
    'sex': np.random.choice(['male', 'female'], 100),
    'smoker': np.random.choice(['yes', 'no'], 100),
    'family_history': np.random.choice(['yes', 'no'], 100),
    'bmi': np.random.uniform(15, 40, 100),
    'cancer_risk': np.random.uniform(0, 1, 100)
}
df = pd.DataFrame(data)

# 2. EDA
print("Shapes:", df.shape)
print("Dtypes:\n", df.dtypes)
print("Describe:\n", df.describe())
print("Correlations:\n", df.corr())

# 3. Data preprocessing
numeric_features = ['age', 'bmi', 'cancer_risk']
categorical_features = ['sex', 'smoker', 'family_history']

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
df['age_group'] = pd.cut(df['age'], bins=[20, 40, 60, 80], labels=[1, 2, 3])
df['bmi_category'] = pd.cut(df['bmi'], bins=[15, 18.5, 25, 30, 40], labels=[1, 2, 3, 4])

numeric_features.extend(['age_group', 'bmi_category'])
categorical_features.extend(['age_group', 'bmi_category'])

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

# 5. Train/test split
X = df.drop('cancer_risk', axis=1)
y = df['cancer_risk']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Model training
model = Pipeline(steps=[('preprocessor', preprocessor),
                      ('regressor', RandomForestRegressor())])
model.fit(X_train, y_train)

# 7. Evaluation
y_pred = model.predict(X_test)
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R²:", r2_score(y_test, y_pred))

# 8. Prediction function
def predict(input_dict):
    input_df = pd.DataFrame([input_dict])
    prediction = model.predict(input_df)
    return prediction[0]

# 9. Save model with joblib
joblib.dump(model, 'cancer_prediction_model.joblib')