# %% imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
import os

# %% data loading
# Generate synthetic dataset
np.random.seed(0)
df = pd.DataFrame({
    'image_path': [f'picsum.photos/seed/image_{i}/256/256' for i in range(1000)],
    'cancer_score': np.random.uniform(0, 1, 1000)
})
print(df.shape, df.head())

# %% [markdown]
# ## 1. Data Loading and Exploration

# %% data loading and exploration
image_paths = df['image_path'].values
cancer_scores = df['cancer_score'].values

# %% [markdown]
# ## 2. EDA
# %% eda
plt.figure(figsize=(10, 6))
sns.histplot(cancer_scores, bins=20)
plt.title('Distribution of Cancer Scores')
plt.show()

# %% [markdown]
# ## 3. Preprocessing
# %% preprocessing
image_data = []
for image_path in image_paths:
    image = cv2.imread(image_path)
    image = cv2.resize(image, (256, 256))
    image_data.append(image)

image_data = np.array(image_data)
print(image_data.shape)

# %% [markdown]
# ## 4. Model Training
# %% training
X_train, X_test, y_train, y_test = train_test_split(image_data, cancer_scores, test_size=0.2, random_state=42)

datagen = ImageDataGenerator(rescale=1./255)
train_generator = datagen.flow(X_train, y_train, batch_size=32)
test_generator = datagen.flow(X_test, y_test, batch_size=32)

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

history = model.fit(train_generator, epochs=10, validation_data=test_generator)

# %% [markdown]
# ## 5. Evaluation
# %% evaluation
y_pred = model.predict(test_generator)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'MSE: {mse}, R2: {r2}')

plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()