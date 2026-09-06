# INF601 - Advanced Programming in Python
# Nicholas Pollard
# Mini Project 1

import os
import requests

BASE = "https://practice.fhsucyber.com"
TOKEN = os.environ.get("PRACTICE_API_TOKEN")


class PracticeHubClient:
    def __init__(self, base_url, token):
        self.base = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {token}"}

    def create_post(self, title, body="", tags=None):
        resp = requests.post(
            f"{self.base}/api/v1/posts",
            headers=self.headers,
            json={"title": title, "body": body, "tags": tags or []}
        )
        resp.raise_for_status()
        return resp.json()

    def list_posts(self, mine=False, tag=None):
        params = {"mine": mine}
        if tag:
            params["tag"] = tag

        resp = requests.get(
            f"{self.base}/api/v1/posts",
            headers=self.headers,
            params=params
        )
        resp.raise_for_status()
        return resp.json()

    def get_post(self, post_id):
        resp = requests.get(
            f"{self.base}/api/v1/posts/{post_id}",
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()

    def update_post(self, post_id, title=None, body=None, tags=None):
        # PATCH only sends the fields that are actually changing.
        data = {}
        if title is not None:
            data["title"] = title
        if body is not None:
            data["body"] = body
        if tags is not None:
            data["tags"] = tags

        resp = requests.patch(
            f"{self.base}/api/v1/posts/{post_id}",
            headers=self.headers,
            json=data
        )
        resp.raise_for_status()
        return resp.json()

    def delete_post(self, post_id):
        resp = requests.delete(
            f"{self.base}/api/v1/posts/{post_id}",
            headers=self.headers
        )
        resp.raise_for_status()
        # A successful delete returns 204 No Content, so there is no
        # JSON body to parse. Just report success.
        return True


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit(
            "PRACTICE_API_TOKEN is not set - see 'Set your token' in Week 2."
        )

    client = PracticeHubClient(BASE, TOKEN)

    # 1. LIST
    everyone = client.list_posts()
    print(f"posts on the hub: {len(everyone)}")

    # 2. CREATE
    new_post = client.create_post(
        "Mini Project 1 CRUD Demo",
        body="This post was created to demonstrate the create step.",
        tags=["demo", "mini-project-1"]
    )
    post_id = new_post["id"]
    print(f"created post {post_id}: {new_post['title']} tags={new_post.get('tags')}")

    # 3. READ (the post we just created)
    fetched = client.get_post(post_id)
    print(f"fetched post {post_id}: {fetched['title']} body={fetched['body']!r}")

    # 4. UPDATE
    updated = client.update_post(
        post_id,
        title="Mini Project 1 CRUD Demo (Updated)",
        body="This post was updated to demonstrate the update step.",
        tags=["demo", "mini-project-1", "updated"]
    )
    print(f"updated post {post_id}: {updated['title']} tags={updated.get('tags')}")

    # 5. READ again to confirm the update stuck
    reread = client.get_post(post_id)
    print(
        f"re-fetched post {post_id}: title={reread['title']!r} "
        f"body={reread['body']!r} tags={reread.get('tags')}"
    )

    # 6. DELETE (clean up after ourselves)
    deleted = client.delete_post(post_id)

    # 7. Confirm deletion
    print(f"deleted post {post_id}: {deleted}")