import joblib
import pandas as pd
from features import extract_features
import time
# Load model and encoder once at import
model = joblib.load("model.pkl")
encoder = joblib.load("content_type_encoder.pkl")

def rank_posts(user_profile: dict, posts: list[dict], author_branch_map: dict = None) -> list[dict]:
    """
    Rank posts based on user profile using trained model.

    :param user_profile: Dict with user's tags, buddies, branches, active hours
    :param posts: List of posts to rank
    :param author_branch_map: Optional dict mapping author_id to branch (defaults to 'CSE')
    :return: List of dicts with post_id and relevance score, sorted by score
    """
    start = time.time()
    feature_rows = []
    post_ids = []
    if not posts:
        return []
    for post in posts:
        author_id = post["author_id"]
        branch = author_branch_map.get(author_id, "CSE") if author_branch_map else "CSE"
        
        features = extract_features(user_profile, post, author_branch=branch)
        post_ids.append(post["post_id"])
        feature_rows.append(features)

    # Convert to DataFrame
    df = pd.DataFrame(feature_rows)

    # One-hot encode content_type
    encoded = encoder.transform(df[["content_type"]])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(["content_type"]))

    df = df.drop(columns=["content_type"]).reset_index(drop=True)
    X = pd.concat([df, encoded_df], axis=1)

    # Predict scores
    scores = model.predict(X)

    # Combine with post IDs and sort
    ranked = sorted(
        [{"post_id": pid, "score": round(score, 4)} for pid, score in zip(post_ids, scores)],
        key=lambda x: x["score"],
        reverse=True
    )
    end = time.time()
    print(f"Ranking completed in {end - start:.3f} seconds")
    return ranked
