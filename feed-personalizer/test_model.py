import joblib
import pandas as pd

# Load trained model and encoder
model = joblib.load("model.pkl")
encoder = joblib.load("content_type_encoder.pkl")

# Define test sample
test_input = {
    "user_follows_tag": True,
    "is_buddy_post": False,
    "content_type": "video",
    "karma": 70,
    "time_match_score": 0.85,
    "author_branch_similarity": True
}

# Convert to DataFrame
df = pd.DataFrame([test_input])

# One-hot encode content_type
encoded_type = encoder.transform(df[["content_type"]])
encoded_df = pd.DataFrame(encoded_type, columns=encoder.get_feature_names_out(["content_type"]))

# Drop original content_type and combine
df = df.drop(columns=["content_type"]).reset_index(drop=True)
X_test = pd.concat([df, encoded_df], axis=1)

# Predict
score = model.predict(X_test)[0]
print(f"Predicted relevance score: {round(score, 4)}")
