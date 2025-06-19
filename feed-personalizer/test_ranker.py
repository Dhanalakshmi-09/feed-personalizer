from ranker import rank_posts

# Sample user profile
user_profile = {
    "branches_of_interest": ["CSE", "AI"],
    "tags_followed": ["coding", "startups", "python"],
    "buddies": ["stu_2010", "stu_3012"],
    "active_hours": ["08:00-11:00", "21:00-23:00"]
}

# Sample posts
posts = [
    {
        "post_id": "post_1001",
        "author_id": "stu_1009",
        "tags": ["internships", "coding"],
        "content_type": "text",
        "karma": 40,
        "created_at": "2024-07-18T09:45:00Z"
    },
    {
        "post_id": "post_1002",
        "author_id": "stu_2010",
        "tags": ["clubs", "events"],
        "content_type": "video",
        "karma": 70,
        "created_at": "2024-07-18T10:30:00Z"
    },
    {
        "post_id": "post_1003",
        "author_id": "stu_3001",
        "tags": ["random"],
        "content_type": "poll",
        "karma": 3,
        "created_at": "2024-07-18T02:00:00Z"
    }
]

# Optional: Map author ID to branch (default is "CSE")
author_branch_map = {
    "stu_1009": "CSE",
    "stu_2010": "ECE",
    "stu_3001": "Mechanical"
}

# Rank the posts
ranked = rank_posts(user_profile, posts, author_branch_map)

# Show results
print("Ranked Posts:")
for post in ranked:
    print(f"Post ID: {post['post_id']} - Score: {post['score']}")
