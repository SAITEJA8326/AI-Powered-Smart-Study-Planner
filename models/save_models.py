import os

def save_model(model, name):
    os.makedirs("outputs/models", exist_ok=True)
    model.save(f"outputs/models/{name}.h5")