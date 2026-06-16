from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
import os

def train_autoencoder(data):
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    input_dim = data_scaled.shape[1]

    input_layer = Input(shape=(input_dim,))
    encoded = Dense(16, activation='relu')(input_layer)
    encoded = Dense(8, activation='relu')(encoded)

    decoded = Dense(16, activation='relu')(encoded)
    decoded = Dense(input_dim, activation='sigmoid')(decoded)

    autoencoder = Model(inputs=input_layer, outputs=decoded)
    autoencoder.compile(optimizer='adam', loss='mse')

    history = autoencoder.fit(
        data_scaled,
        data_scaled,
        epochs=5,
        batch_size=32,
        validation_split=0.2
    )

    os.makedirs("outputs/plots", exist_ok=True)

    plt.plot(history.history['loss'], label='Train')
    plt.plot(history.history['val_loss'], label='Val')
    plt.legend()
    plt.title("Autoencoder Loss")
    plt.savefig("outputs/plots/ae_loss.png")
    plt.close()

    recon = autoencoder.predict(data_scaled)
    mse = np.mean((data_scaled - recon)**2, axis=1)

    return autoencoder, scaler, mse