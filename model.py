import numpy as np

class LR:
    def __init__(self):
        self.weights = None
        self.X_data = None
        self.y_data = None
        self.X_mean = None
        self.X_std = None
        self.y_mean = None
        self.y_std = None

    def add_bias(self, X):
        return np.c_[np.ones((X.shape[0], 1)), X]

    def normalize(self, X, y):
        if self.X_mean is None:
            self.X_mean = np.mean(X, axis=0)
            self.X_std = np.std(X, axis=0)
            self.y_mean = np.mean(y)
            self.y_std = np.std(y)

        X_normalized = (X - self.X_mean) / (self.X_std + 1e-8)
        y_normalized = (y - self.y_mean) / (self.y_std + 1e-8)

        return X_normalized, y_normalized

    def denormalize_predictions(self, y_pred_normalized):
        return y_pred_normalized * self.y_std + self.y_mean

    def fit(self, X, y, epochs=1000, learning_rate=0.05):
        if self.X_data is None:
            self.X_data = X
            self.y_data = y
        else:
            self.X_data = np.vstack((self.X_data, X))
            self.y_data = np.vstack((self.y_data, y))

        X_normalized, y_normalized = self.normalize(self.X_data, self.y_data)
        X_normalized = self.add_bias(X_normalized)

        if self.weights is None:
            self.weights = np.zeros((X_normalized.shape[1], 1))

        for _ in range(epochs):
            predictions = X_normalized.dot(self.weights)
            error = predictions - y_normalized
            gradients = X_normalized.T.dot(error) / X_normalized.shape[0]
            self.weights -= learning_rate * gradients

            learning_rate *= 0.99

    def predict(self, X):
        X_normalized = (X - self.X_mean) / (self.X_std + 1e-8)
        X_normalized = self.add_bias(X_normalized)
        y_pred_normalized = X_normalized.dot(self.weights)
        return self.denormalize_predictions(y_pred_normalized)