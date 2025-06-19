import datetime

def extract_features(user_profile, post, author_branch):
    # Feature 1: Check if user follows any tags in the post
    user_tags = user_profile.get("tags_followed", [])
    post_tags = post.get("tags", [])
    user_follows_tag = any(tag in user_tags for tag in post_tags)

    # Feature 2: Is the post from a buddy?
    buddies = user_profile.get("buddies", [])
    is_buddy_post = post.get("author_id") in buddies

    # Feature 3: Content type (categorical)
    content_type = post.get("content_type", "text")

    # Feature 4: Karma (numeric)
    karma = post.get("karma", 0)

    # Feature 5: Time match score
    active_hours = user_profile.get("active_hours", [])
    try:
        post_hour = datetime.datetime.fromisoformat(post["created_at"].replace("Z", "+00:00")).hour
    except Exception:
        post_hour = -1

    time_match_score = 0
    if post_hour != -1:
        for interval in active_hours:
            try:
                start_str, end_str = interval.split("-")
                start = int(start_str.split(":")[0])
                end = int(end_str.split(":")[0])
                if start <= post_hour <= end:
                    time_match_score = 1
                    break
            except Exception:
                continue

    # Feature 6: Author branch similarity
    user_branches = user_profile.get("branches_of_interest", [])
    author_branch_similarity = author_branch in user_branches if author_branch else False

    return {
        "user_follows_tag": user_follows_tag,
        "is_buddy_post": is_buddy_post,
        "content_type": content_type,
        "karma": karma,
        "time_match_score": time_match_score,
        "author_branch_similarity": author_branch_similarity
    }
