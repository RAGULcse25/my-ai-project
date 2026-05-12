import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import joblib
from PIL import Image
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import requests
from io import BytesIO

# 1. Generate/load synthetic dataset
np.random.seed(0)
df = pd.DataFrame({
    'image_url': [f'https://picsum.photos/seed/image_{i}/200/200' for i in range(100)],
    'tumor_size': np.random.uniform(0, 10, 100),
    'age': np.random.uniform(20, 80, 100),
    'sex': np.random.choice(['male', 'female'], 100),
    'cancer_type': np.random.choice(['breast', 'lung', 'colon'], 100),
    'cancer_stage': np.random.uniform(0, 4, 100)
})

# 2. EDA
print("Shapes:", df.shape)
print("Dtypes:\n", df.dtypes)
print("Describe:\n", df.describe())
print("Correlations:\n", df.corr())

# 3. Data preprocessing
numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
categorical_features = df.select_dtypes(include=['object']).columns

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
def extract_features_from_image(url):
    img = Image.open(BytesIO(requests.get(url).content))
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    model = ResNet50(weights='imagenet')
    features = model.predict(img_array)
    return features.flatten()

df['image_features'] = df['image_url'].apply(extract_features_from_image)

# 5. Train/test split
X = df.drop('cancer_stage', axis=1)
y = df['cancer_stage']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Model training
X_train = preprocessor.fit_transform(X_train)
X_test = preprocessor.transform(X_test)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluation
y_pred = model.predict(X_test)
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R²:", r2_score(y_test, y_pred))

# 8. Prediction function
def predict(input_dict):
    input_df = pd.DataFrame([input_dict])
    input_df['image_features'] = input_df['image_url'].apply(extract_features_from_image)
    input_df = input_df.drop('image_url', axis=1)
    input_df = preprocessor.transform(input_df)
    prediction = model.predict(input_df)
    return prediction

# 9. Save model with joblib
joblib.dump(model, 'cancer_prediction_model.joblib')
joblib.dump(preprocessor, 'preprocessor.joblib')