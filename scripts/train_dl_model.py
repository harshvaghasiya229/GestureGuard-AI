import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv("data/gesture_data.csv", header=None)

X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Encode labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Save label mapping
np.save("data/labels.npy", encoder.classes_)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2
)

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation="relu", input_shape=(X.shape[1],)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(len(set(y_encoded)), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Train
model.fit(X_train, y_train, epochs=20, batch_size=16)

# Evaluate
loss, acc = model.evaluate(X_test, y_test)
print("Accuracy:", acc)

# Save model
model.save("data/gesture_dl_model.h5")