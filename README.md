# Mini Project 1 - API Client

## Description

This project implements `PracticeHubClient`, a small Python class that
performs full CRUD (Create, Read, Update, Delete) operations against the
Practice Hub API (`https://practice.fhsucyber.com`) using the `requests`
library. It was built on top of the professor's starter `client.py`, which
already provided `create_post()` and `list_posts()`; this project adds
`get_post()`, `update_post()`, `delete_post()`, and graceful handling of
the API's error responses.

## Features

- `PracticeHubClient` stores the API base URL and an `Authorization: Bearer`
  header built from an API token.
- Full CRUD support: create, list, read, update, and delete posts.
- A single internal `_request()` helper that all methods route through,
  which centralizes HTTP error handling instead of repeating the same
  status-code checks in every method.
- Specific, human-readable error messages for 401, 403, 404, and 422
  responses instead of raw `requests` tracebacks.
- A `__main__` block that runs a full, self-cleaning CRUD demonstration.

## Requirements

- Python 3.9+
- `requests` (see `requirements.txt`)

## Installation

Install the one dependency this project uses:

```
pip install -r requirements.txt
```

## Setting the API Token

The client reads your API token from the `PRACTICE_API_TOKEN` environment
variable. It is **never** hard-coded in the source. Set it in your shell
before running the program.

**Windows PowerShell:**

```powershell
$env:PRACTICE_API_TOKEN = "your-token-here"
```

**macOS/Linux (bash/zsh):**

```bash
export PRACTICE_API_TOKEN="your-token-here"
```

This only sets the variable for the current terminal session. If you close
the terminal, you'll need to set it again before running the program.

## Running the Program

With the token set and the dependency installed, run:

```
python client.py
```

This performs a full CRUD cycle against a temporary post named
**"Mini Project 1 CRUD Demo"** and prints each step: listing existing
posts, creating the demo post, reading it back, updating it, reading the
updated values, and finally deleting the post it created (so it does not
leave anything behind on the server).

## CRUD Operations

`PracticeHubClient` implements the following methods, each corresponding
to one Practice Hub endpoint:

| Method | HTTP Verb | Endpoint | Purpose |
|---|---|---|---|
| `create_post(title, body="", tags=None)` | POST | `/api/v1/posts` | Create a new post |
| `list_posts(mine=False, tag=None)` | GET | `/api/v1/posts` | List posts, optionally filtered to your own or by tag |
| `get_post(post_id)` | GET | `/api/v1/posts/{post_id}` | Fetch a single post by id |
| `update_post(post_id, title=None, body=None, tags=None)` | PATCH | `/api/v1/posts/{post_id}` | Update only the fields provided |
| `delete_post(post_id)` | DELETE | `/api/v1/posts/{post_id}` | Delete a post |

`update_post()` uses **PATCH** rather than PUT because PATCH lets us send
only the fields that are actually changing, instead of having to resend
the entire post every time.

`delete_post()` returns `True` on success. A successful delete returns
HTTP 204 No Content, which has no JSON body, so the method does not try
to call `.json()` on the response.

## Error Handling

All requests go through a private `_request()` helper on
`PracticeHubClient`. This keeps the status-code handling in one place
instead of duplicating it in every CRUD method. `_request()` checks the
response and raises a `PracticeHubError` (a plain `Exception` subclass)
with a clear message for these cases:

- **401 Unauthorized** - authentication failed; check that
  `PRACTICE_API_TOKEN` is set to a valid token.
- **403 Forbidden** - you can only modify or delete your own posts.
- **404 Not Found** - the requested post does not exist.
- **422 Unprocessable Entity** - the API rejected the data; the error
  message includes the `detail` field from the API's response so you can
  see exactly what failed validation.
- Any other unexpected status code raises `PracticeHubError` with the
  status code and response body included, rather than being swallowed.

None of these cases raise a raw `requests` exception/traceback - they are
all caught and re-raised as a `PracticeHubError` with a readable message.

These four required error paths were manually verified during
development (using a temporary invalid token, a nonexistent post id, an
intentionally invalid post body, and an attempt to update another user's
post) and all behaved as expected. That testing was done separately from
the normal program run - `python client.py` always performs a clean,
successful CRUD demonstration and does not intentionally trigger errors.

## Project Files

- `client.py` - the `PracticeHubClient` class and the CRUD demonstration.
- `requirements.txt` - the single dependency (`requests`).
- `.gitignore` - excludes `.env`, `scratch.http`, `__pycache__/`, and `*.pyc`.
- `README.md` - this file.

## AI Usage

I used **Claude Code** (Anthropic's AI coding assistant) while building
this project. Specifically, Claude Code helped me:

- Implement and scaffold the CRUD client methods (`get_post`,
  `update_post`, `delete_post`) on top of the professor's starter code.
- Implement the error-handling helper (`_request()` /
  `PracticeHubError`) that translates 401/403/404/422 responses into
  readable messages.
- Test and debug the project, including manually exercising each of the
  required error paths (401, 403, 404, 422) against the live API without
  leaving bad data behind or modifying another user's content.
- Prepare this documentation (`README.md`).

I reviewed all of the generated code and I am responsible for
understanding every method submitted in this project. I did not
personally type the code that Claude generated, and I am not claiming
otherwise - but I read through it, tested it myself, and can explain how
each method and the error-handling helper work.
