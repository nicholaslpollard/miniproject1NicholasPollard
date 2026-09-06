# INF601 - Advanced Programming in Python
# Nicholas Pollard
# Mini Project 1

import os
import requests

BASE = "https://practice.fhsucyber.com"
TOKEN = os.environ.get("PRACTICE_API_TOKEN")


class PracticeHubError(Exception):
    """Raised for a Practice Hub API error we can give a clear message for."""


class PracticeHubClient:
    def __init__(self, base_url, token):
        self.base = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {token}"}

    def _request(self, method, path, **kwargs):
        """Send one HTTP request and translate error responses into a
        PracticeHubError with a message a student can understand, instead
        of letting a raw requests exception/traceback bubble up."""
        resp = requests.request(method, f"{self.base}{path}", headers=self.headers, **kwargs)

        if resp.ok:
            return resp

        if resp.status_code == 401:
            raise PracticeHubError(
                "401 Unauthorized: authentication failed. Check that "
                "PRACTICE_API_TOKEN is set to a valid token."
            )
        if resp.status_code == 403:
            raise PracticeHubError(
                "403 Forbidden: you can only modify or delete your own posts."
            )
        if resp.status_code == 404:
            raise PracticeHubError(
                "404 Not Found: the requested post was not found."
            )
        if resp.status_code == 422:
            try:
                detail = resp.json().get("detail", "no detail provided")
            except ValueError:
                detail = "no detail provided"
            raise PracticeHubError(f"422 Unprocessable Entity: {detail}")

        # Anything else: don't hide the status code, but don't let a raw
        # requests traceback be the only thing the caller sees either.
        raise PracticeHubError(
            f"Unexpected HTTP {resp.status_code} error from Practice Hub: {resp.text}"
        )

    def create_post(self, title, body="", tags=None):
        resp = self._request(
            "POST",
            "/api/v1/posts",
            json={"title": title, "body": body, "tags": tags or []}
        )
        return resp.json()

    def list_posts(self, mine=False, tag=None):
        params = {"mine": mine}
        if tag:
            params["tag"] = tag

        resp = self._request("GET", "/api/v1/posts", params=params)
        return resp.json()

    def get_post(self, post_id):
        resp = self._request("GET", f"/api/v1/posts/{post_id}")
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

        resp = self._request("PATCH", f"/api/v1/posts/{post_id}", json=data)
        return resp.json()

    def delete_post(self, post_id):
        self._request("DELETE", f"/api/v1/posts/{post_id}")
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
