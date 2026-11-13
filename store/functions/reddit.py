
import requests


def get_reddit_posts():
    """Fetch Reddit posts or use sample data if Reddit blocks access."""

    url = "https://www.reddit.com/r/ecommerce/.json?limit=10"

    headers = {
        "User-Agent": "JongwaStore/1.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

    except requests.RequestException:
        # Sample JSON data for development and testing when Reddit blocks access.
        data = {
            "data": {
                "children": [
                    {
                        "data": {
                            "title": "[SAMPLE DATA] Starting an online store",
                            "author": "JongwaStoreDemo",
                            "url": "https://www.reddit.com/r/ecommerce/"
                        }
                    },
                    {
                        "data": {
                            "title": "[SAMPLE DATA] Tips for ecommerce beginners",
                            "author": "StoreDemo",
                            "url": "https://www.reddit.com/r/ecommerce/"
                        }
                    }
                ]
            }
        }

    posts = []

    for item in data["data"]["children"]:
        post = item["data"]

        posts.append({
            "title": post["title"],
            "author": post["author"],
            "url": post["url"]
        })

    return posts
