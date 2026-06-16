import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
import os

def create_sequences(data, time_steps=5):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i+time_steps])
        y.append(data[i+time_steps])
    return np.array(X), np.array(y)

def train_lstm(data):
    X_seq, y_seq = create_sequences(data)

    model = Sequential([
        LSTM(50, activation='relu', input_shape=(X_seq.shape[1], 1)),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    history = model.fit(X_seq, y_seq, epochs=10, batch_size=32)

    os.makedirs("outputs/plots", exist_ok=True)

    plt.plot(history.history['loss'])
    plt.title("LSTM Loss")
    plt.savefig("outputs/plots/lstm_loss.png")
    plt.close()

    return model