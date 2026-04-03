import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib  # to save model

# Load data
data = pd.read_csv('Crop_recommendation.csv')

# Handling missing values (if any)
data = data.dropna()  # or fillna with median

# Feature / target
features = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
labels = data['label']

# Possible feature scaling
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(features_scaled, labels, test_size=0.2, random_state=42)

# Hyperparameter tuning
rf = RandomForestClassifier(random_state=42)
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
}
grid = GridSearchCV(rf, param_grid, cv=5, n_jobs=-1, verbose=1)
grid.fit(X_train, y_train)

best_model = grid.best_estimator_

# Evaluate
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Best model accuracy: {accuracy:.2f}")

# Feature importance
importances = best_model.feature_importances_
feature_names = features.columns
for name, imp in zip(feature_names, importances):
    print(f"{name}: {imp:.3f}")

# Save model & scaler
joblib.dump(best_model, 'crop_rf_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Recommendation function
def get_crop_recommendation(N, P, K, temperature, humidity, ph, rainfall):
    user_df = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]], 
                           columns=feature_names)
    user_scaled = scaler.transform(user_df)
    prediction = best_model.predict(user_scaled)[0]
    # Also get feature importances to explain
    # maybe partial explanation:
    # sort top features
    imp = dict(zip(feature_names, best_model.feature_importances_))
    sorted_imp = sorted(imp.items(), key=lambda x: x[1], reverse=True)
    top2 = sorted_imp[:2]
    explanation = f"Important Reasons: {top2[0][0]}, {top2[1][0]}"
    return prediction, explanation

# Example usage
crop, reason = get_crop_recommendation(50, 50, 50, 25, 75, 6.5, 150)
print(f"Recommended Crop: {crop}")
print(reason)
