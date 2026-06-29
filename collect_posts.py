import praw
import csv
import os
import time
from datetime import datetime

# -------------------------------------------------------------------
# Reddit API credentials
# Create an app at https://www.reddit.com/prefs/apps to get these
# -------------------------------------------------------------------
CLIENT_ID = "mgs7ifOByh_fF_1LzzUVDw"
CLIENT_SECRET = "qptBjwIeBTKqqdWl3-Sd9nGtQcbAjw"
USER_AGENT = "cogs108 script by u/hiyossssu"

SUBREDDIT = "leagueoflegends"
TARGET_PER_SOURCE = 100      # 4 sources x 50 = 200 posts
OUTPUT_FILE = "data/raw_posts.csv"

# Each source is (sort_method, time_filter_or_None)
SOURCES = [
    ("hot",          None),
    ("new",          None),
    ("top",          "month"),
    ("controversial","month"),
]

FIELDNAMES = [
    "post_id",
    "source",       # which sort method it came from
    "flair",
    "title",
    "body",
    "score",
    "upvote_ratio",
    "num_comments",
    "created_utc",
    "url",
    "label",        # blank — fill in during annotation
]


def clean_text(text: str) -> str:
    """Strip newlines and extra whitespace so CSV cells stay clean."""
    if not text:
        return ""
    return " ".join(text.split())


def fetch_posts(reddit: praw.Reddit, subreddit_name: str) -> list[dict]:
    sub = reddit.subreddit(subreddit_name)
    seen_ids: set[str] = set()
    all_posts: list[dict] = []

    for sort_method, time_filter in SOURCES:
        print(f"  Fetching '{sort_method}' (time_filter={time_filter}) ...")
        collected = 0

        # PRAW needs time_filter only for top/controversial
        kwargs = {"limit": TARGET_PER_SOURCE * 3}  # fetch extra to cover deletions/dupes
        if time_filter:
            kwargs["time_filter"] = time_filter

        listing = getattr(sub, sort_method)(**kwargs)

        for post in listing:
            if collected >= TARGET_PER_SOURCE:
                break
            if post.id in seen_ids:
                continue
            if post.is_self and not post.selftext:
                continue  # skip deleted/empty text posts
            if post.selftext in ("[deleted]", "[removed]"):
                continue

            seen_ids.add(post.id)
            all_posts.append({
                "post_id":      post.id,
                "source":       sort_method,
                "flair":        post.link_flair_text or "",
                "title":        clean_text(post.title),
                "body":         clean_text(post.selftext),
                "score":        post.score,
                "upvote_ratio": post.upvote_ratio,
                "num_comments": post.num_comments,
                "created_utc":  datetime.utcfromtimestamp(post.created_utc).strftime("%Y-%m-%d %H:%M"),
                "url":          f"https://reddit.com{post.permalink}",
                "label":        "",
            })
            collected += 1

        print(f"    Collected {collected} posts from '{sort_method}'.")
        time.sleep(1)  # be polite to the API

    return all_posts


def save_csv(posts: list[dict], filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(posts)
    print(f"\nSaved {len(posts)} posts to '{filepath}'.")


def main() -> None:
    if "YOUR_CLIENT_ID" in CLIENT_ID:
        raise ValueError(
            "Fill in CLIENT_ID, CLIENT_SECRET, and USER_AGENT at the top of this file "
            "before running. See https://www.reddit.com/prefs/apps"
        )

    print(f"Connecting to Reddit API ...")
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )

    print(f"Fetching posts from r/{SUBREDDIT} ...\n")
    posts = fetch_posts(reddit, SUBREDDIT)

    print(f"\nTotal unique posts collected: {len(posts)}")
    save_csv(posts, OUTPUT_FILE)

    # Quick flair breakdown so you can see topic variety
    from collections import Counter
    flair_counts = Counter(p["flair"] or "No Flair" for p in posts)
    print("\nFlair breakdown:")
    for flair, count in flair_counts.most_common():
        print(f"  {flair:<30} {count}")


if __name__ == "__main__":
    main()
