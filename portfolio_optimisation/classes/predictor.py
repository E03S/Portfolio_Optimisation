import pickle
from catboost import CatBoostRegressor

class FinancialPredictor:
    def __init__(self, regressor_path, preprocessor_path):
        self.model = CatBoostRegressor().load_model(regressor_path)

        with open(preprocessor_path, "rb") as f:
            self.preprocessor = pickle.load(f)

    def predict(self, X):
        X_processed = self.preprocessor.transform(X)
        return self.model.predict(X_processed)
