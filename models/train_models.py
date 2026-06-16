import pandas as pd
import numpy as np
import tensorflow as tf
import os

# Create model folder
MODEL_PATH = "models/saved_models/"
os.makedirs(MODEL_PATH, exist_ok=True)

# Load dataset
df = pd.read_excel("dataset/student_dataset_25000 (1).xlsx")

# Normalize column names
df.columns = df.columns.str.lower().str.strip()

print("Available Columns:", df.columns)

# ✅ EXACT 13 SUBTOPICS (based on your dataset)
columns = [
    'maths_s&p',
    'maths_trigonometry',
    'maths_calculus',
    'maths_algebra',
    'maths_coordinate',
    'physics_optics',
    'physics_mechanics',
    'physics_thermodynamics',
    'physics_waves',
    'physics_electricity',
    'chemistry_inorganic',
    'chemistry_organic',
    'chemistry_physical'
]

# Check missing columns
missing = [col for col in columns if col not in df.columns]
if missing:
    print("❌ Missing columns:", missing)
    exit()

print("✅ Using Columns:", columns)

# Input features
X = df[columns].fillna(0).values

# Target = average score
y = np.mean(X, axis=1)

print("Input Shape:", X.shape)

# ============================
# 🔥 Neural Network Model
# ============================
nn = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(13,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

nn.compile(optimizer='adam', loss='mse')

print("🚀 Training Neural Network...")
nn.fit(X, y, epochs=5, batch_size=32)

# Save model
nn.save(os.path.join(MODEL_PATH, "nn_model.h5"))

# ============================
# 🔥 Autoencoder Model
# ============================
input_layer = tf.keras.Input(shape=(13,))
encoded = tf.keras.layers.Dense(16, activation='relu')(input_layer)
decoded = tf.keras.layers.Dense(13, activation='sigmoid')(encoded)

ae = tf.keras.Model(input_layer, decoded)
ae.compile(optimizer='adam', loss='mse')

print("🚀 Training Autoencoder...")
ae.fit(X, X, epochs=5, batch_size=32)

# Save model
ae.save(os.path.join(MODEL_PATH, "autoencoder.h5"))

print("\n✅ SUCCESS: Models trained and saved correctly!")