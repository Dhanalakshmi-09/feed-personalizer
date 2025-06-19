import json
import random

def simulate_training_data(n_samples=1000):
    branches = ["CSE", "AI", "ECE", "ME"]
    tags = ["coding", "startups", "python", "internships", "clubs", "events"]
    content_types = ["text", "image", "poll", "video"]
    data=[]
    for _ in range(n_samples):
        # Random feature values
        user_branch = random.choice(branches)
        post_branch = random.choice(branches)
        is_buddy = random.choice([True, False])
        user_tags = random.sample(tags, k=random.randint(1, 3))
        post_tags = random.sample(tags, k=random.randint(1, 2))
        user_follows_tag = any(tag in user_tags for tag in post_tags)
        content_type = random.choice(content_types)
        karma = random.randint(0, 100)
        time_score = round(random.uniform(0, 1), 2)

        # Simulate label (likelihood of engagement)
        # Relevance label: weighted sum simulation
        label = (
            0.3 * int(user_follows_tag) +
            0.2 * int(is_buddy) +
            0.1 * (karma / 100) +
            0.2 * time_score +
            0.2 * int(user_branch == post_branch)
        )
        label = round(label, 2)

        data.append({
            "features": {
            "user_follows_tag": user_follows_tag,
            "is_buddy_post": is_buddy,
            "content_type": content_type,
            "karma": karma,
            "time_match_score": time_score,
            "author_branch_similarity": user_branch == post_branch
            },
            "label": label
        })

    with open("training_data.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated {n_samples} training samples in training_data.json")

# Run the simulation
simulate_training_data()
