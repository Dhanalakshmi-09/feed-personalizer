from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal
import joblib
from ranker import rank_posts

# -------------------------------
# Load model and encoder
# -------------------------------
model = joblib.load("model.pkl")
encoder = joblib.load("content_type_encoder.pkl")

# -------------------------------
# FastAPI app
# -------------------------------
app = FastAPI(title="Feed Personalizer API")

# -------------------------------
# Pydantic Models for API
# -------------------------------
class PostInput(BaseModel):
    post_id: str
    author_id: str
    tags: List[str]
    content_type: Literal["text", "image", "poll", "video"]
    karma: int
    created_at: str

class UserProfile(BaseModel):
    branches_of_interest: List[str]
    tags_followed: List[str]
    buddies: List[str]
    active_hours: List[str]

class FeedRequest(BaseModel):
    user_id: str
    user_profile: UserProfile
    posts: List[PostInput]

class RankedPost(BaseModel):
    post_id: str
    score: float

class FeedResponse(BaseModel):
    user_id: str
    ranked_posts: List[RankedPost]
    status: Literal["ranked", "error"]

# -------------------------------
# Main API endpoint
# -------------------------------
@app.post("/rank-feed", response_model=FeedResponse)
def rank_feed(payload: FeedRequest):
    try:
        # Convert posts to list of dicts
        posts = [post.dict() for post in payload.posts]
        user_profile = payload.user_profile.dict()

        # Rank the posts
        ranked_posts = rank_posts(user_profile, posts)

        return FeedResponse(
            user_id=payload.user_id,
            ranked_posts=ranked_posts,
            status="ranked"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------
# Health check
# -------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------------
# Version endpoint
# -------------------------------
@app.get("/version")
def version():
    return {"model_version": "1.0.0"}
