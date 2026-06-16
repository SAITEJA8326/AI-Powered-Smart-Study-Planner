import tensorflow as tf
import numpy as np
import os

MODEL_PATH = "models/saved_models/"

def get_dl_insights(subtopic_scores):
    try:
        nn = tf.keras.models.load_model(os.path.join(MODEL_PATH, "nn_model.h5"))
        ae = tf.keras.models.load_model(os.path.join(MODEL_PATH, "autoencoder.h5"))
    except:
        return None, None

    scores_array = np.array([subtopic_scores])

    prediction = nn.predict(scores_array, verbose=0)
    reconstruction = ae.predict(scores_array, verbose=0)

    mse = np.mean(np.square(scores_array - reconstruction))

    return float(prediction[0][0]), float(mse)