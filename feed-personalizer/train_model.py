import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
import joblib

# Load training data
with open("training_data.json", "r") as f:
    data = json.load(f)

# Extract features and labels
feature_dicts = [sample["features"] for sample in data]
labels = [sample["label"] for sample in data]

# Convert to DataFrame
df = pd.DataFrame(feature_dicts)

# One-hot encode 'content_type'
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoded_content_type = encoder.fit_transform(df[["content_type"]])
encoded_df = pd.DataFrame(encoded_content_type, columns=encoder.get_feature_names_out(["content_type"]))

# Drop original content_type and combine
df = df.drop(columns=["content_type"])
X = pd.concat([df.reset_index(drop=True), encoded_df], axis=1)
y = np.array(labels)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model and encoder
joblib.dump(model, "model.pkl")
joblib.dump(encoder, "content_type_encoder.pkl")

print("✅ Model training complete. Saved as model.pkl")
