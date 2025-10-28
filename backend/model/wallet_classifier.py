import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class WalletClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self._train_initial_model()
    
    def _train_initial_model(self):
        X_train = np.array([
            [10, 5, 50000, 0.2, 15, 3],
            [100, 50, 500000, 0.8, 200, 20],
            [5, 2, 10000, 0.1, 8, 1],
            [200, 150, 1000000, 0.9, 500, 50],
            [50, 30, 200000, 0.6, 100, 15],
            [3, 1, 5000, 0.05, 5, 0],
            [150, 100, 800000, 0.85, 300, 40],
            [20, 10, 100000, 0.3, 50, 5],
            [8, 4, 30000, 0.15, 12, 2],
            [180, 120, 900000, 0.88, 400, 45]
        ])
        
        y_train = np.array([0, 2, 0, 2, 1, 0, 2, 1, 0, 2])
        
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        self.is_trained = True
    
    def extract_features(self, wallet_data):
        features = [
            wallet_data.get('transaction_count', 0),
            wallet_data.get('unique_addresses', 0),
            wallet_data.get('total_volume', 0),
            wallet_data.get('mixer_probability', 0),
            wallet_data.get('avg_transaction_size', 0),
            wallet_data.get('suspicious_flags', 0)
        ]
        return np.array(features).reshape(1, -1)
    
    def classify(self, wallet_data):
        features = self.extract_features(wallet_data)
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        labels = {0: 'Personal', 1: 'Exchange', 2: 'Suspicious'}
        
        return {
            'classification': labels[prediction],
            'confidence': float(max(probabilities)),
            'probabilities': {
                'personal': float(probabilities[0]),
                'exchange': float(probabilities[1]),
                'suspicious': float(probabilities[2])
            }
        }