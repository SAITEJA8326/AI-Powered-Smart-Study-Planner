def evaluate(model, X_test, y_test):
    loss, mae = model.evaluate(X_test, y_test)
    print("Loss:", loss)
    print("MAE:", mae)