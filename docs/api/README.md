# REST API contract

[openapi.yaml](openapi.yaml) is the draft contract between the React client and the FastAPI
backend (issue #14). The backend, the frontend and the intelligence layer all build against it.

Once the endpoints exist, FastAPI generates the live schema at `/openapi.json` and the docs at
`/docs`. If the code and this file disagree, fix whichever is wrong in the same pull request.

**Viewing it:** paste the file into [editor.swagger.io](https://editor.swagger.io), or open it
in VS Code with the *OpenAPI (Swagger) Editor* extension.

## Endpoints

All paths are under `/api/v1`, except `/health`. Every endpoint needs
`Authorization: Bearer <access token>` except `/health`, `/auth/register`, `/auth/login`,
`/auth/refresh` and `/auth/logout`. In particular, `/auth/me` needs one.

| Requirement | Method and path | What it does |
| --- | --- | --- |
| H1 | `POST /auth/register` | Create an account (password at least 8 characters) |
| H1 | `POST /auth/login` | Get an access token and a refresh-token cookie |
| H1 | `POST /auth/refresh` | Swap the refresh-token cookie for a new access token |
| H1 | `POST /auth/logout` | Revoke the refresh token on the server and clear the cookie |
| H1 | `GET /auth/me` | The logged-in user |
| H2 | `GET /notes` | List notes, newest entry date first, filterable by `from` and `to` |
| H2 | `POST /notes` | Create a note; suggestions start in the background |
| H2 | `GET /notes/{id}` | A note with its accepted links |
| H2 | `PATCH /notes/{id}` | Edit a note; changed content replaces its pending suggestions |
| H2 | `DELETE /notes/{id}` | Delete a note and its links |
| H3 | `GET /notes/{id}/suggestions` | The note's `suggestion_status` and up to 5 suggestions made for it |
| H4 | `GET /suggestions` | Review queue: all pending suggestions, best first |
| H4 | `POST /suggestions/{id}/accept` | Accept a link; it appears in the graph |
| H4 | `POST /suggestions/{id}/reject` | Reject a link; the pair is never suggested again |
| H5 | `GET /graph` | Notes (with a short preview) and accepted links, filterable by date |
| H6 | `GET`, `POST /chat/sessions` | List sessions (most recently used first) or start one |
| H6 | `GET`, `DELETE /chat/sessions/{id}` | A session with its messages, or delete it |
| H6 | `POST /chat/sessions/{id}/messages` | Ask a question; returns the answer with cited notes |
| Privacy | `GET /account/export` | Download all of the user's data as JSON |
| Privacy | `POST /account/delete` | Delete the account and all data (password needed again) |
| #16 | `GET /health` | Status of the API, Neo4j and PostgreSQL; 503 if any is down |

## Sessions

H1 and #20 need sessions that expire after inactivity and a logout that works on the server,
so there are two tokens:

| | Access token | Refresh token |
| --- | --- | --- |
| Format | JWT | Random, opaque string |
| Where the client keeps it | In memory | `nodebook_refresh` httpOnly cookie, `Path=/api/v1/auth` |
| Lifetime | `ACCESS_TOKEN_EXPIRE_MINUTES` (default 15) | Until unused for `REFRESH_TOKEN_IDLE_MINUTES` (default 10080, i.e. 7 days) |
| Server side | Nothing stored | Stored hashed in PostgreSQL; rotated on every refresh; revoked on logout |

**Client flow:**
1. A request returns 401 `unauthorized`.
2. The client calls `POST /auth/refresh` once, then retries the request.
3. If the refresh also returns 401, the session has expired, and the client sends the user to login (#26).
   **Only a 401 does this.** A 5xx or network error during the refresh keeps the session: show an
   error and try again later.

A new tab has no access token yet, so on load it calls `POST /auth/refresh` to pick up the existing session.

**Deleted accounts.** Access tokens aren't stored, so on every bearer endpoint the backend also checks
that the token's user still exists (one primary-key lookup). After `POST /account/delete`, other tabs
and devices get 401 straight away instead of writing data for up to 15 minutes. Account deletion runs
in this order:
1. Delete the PostgreSQL user row, which cascades to chat history and refresh tokens. From here on,
   all requests with that user's tokens get 401.
2. Cancel the user's suggestion jobs. Each job also checks that its user still exists before writing.
3. Delete everything with that `user_id` in Neo4j.

A periodic cleanup deletes Neo4j nodes whose `user_id` has no user. That catches a request that passed
its user check just before step 1.

**Send credentials on four requests.** The client (`:5173`) and the API (`:8000`) are different
origins. The browser only stores or sends the cookie on requests made with
`fetch(..., { credentials: "include" })`:

| Request | Why it needs credentials |
| --- | --- |
| `POST /auth/login` | Otherwise the browser ignores the `Set-Cookie` and every refresh fails |
| `POST /auth/refresh` | Sends the cookie and stores the rotated one |
| `POST /auth/logout` | Sends the cookie to revoke, and clears it |
| `POST /account/delete` | Clears the cookie |

The backend's CORS allows credentials, and only from the origins in `CORS_ORIGINS`, never `*`.

**Only one refresh at a time.** Each refresh token works once, so two refreshes with the same cookie
would make the second one fail with 401 and log the user out. The client prevents this in two ways:
- **Within a tab:** keep one shared refresh promise. Every request that gets a 401 while a refresh
  is running waits for that same refresh, then retries.
- **Across tabs:** run the refresh inside `navigator.locks.request("nodebook-refresh", ...)`. Tabs
  share one cookie jar, so a tab that waited for the lock sends the cookie the previous tab just
  received, and its refresh succeeds too.
- **Logout follows the same rules:** wait for any refresh running in the tab, then send logout inside
  the same `nodebook-refresh` lock. Otherwise a refresh could rotate the token, logout could revoke
  the old one, and the refresh response could then set the new cookie, leaving the user logged in.

**Clearing the cookie.** Logout and account deletion send
`Set-Cookie: nodebook_refresh=; Path=/api/v1/auth; Max-Age=0`, with the same `Path` the cookie was
set with. Starlette's `delete_cookie` defaults to `Path=/`, which wouldn't clear it, so pass
`path="/api/v1/auth"`.

## Suggestions

- **Direction:** `source` is the note whose save produced the suggestion, and `target` is the
  candidate. `type` reads from source to target, so "A `supports` B" means A supports B.
- **One link per pair:** two notes have at most one link between them, in either direction. A pair
  that already has a link, even a rejected one, is never suggested again.
- **Per-note endpoint:** `GET /notes/{id}/suggestions` only returns suggestions whose `source` is
  that note, so there are never more than 5. Suggestions where the note is the `target` are in
  the review queue.
- **Editing:** when a note's content changes, every link to or from it that is still `suggested` is
  deleted, and new suggestions are generated. Accepted and rejected links are always kept.
- **Job status:** each note stores `suggestion_status` (`pending`, `ready` or `failed`), so the
  client knows whether to keep polling. Zero suggestions alone can't tell these apart.

## Errors

Every error, including validation errors, unknown paths and wrong methods, has the same shape. The
one exception is `/health`: its 503 uses the `Health` schema, so it can say which dependency is down.

```json
{
  "error": {
    "code": "validation_error",
    "message": "The request is invalid.",
    "details": [{ "field": "body.password", "message": "String should have at least 8 characters" }]
  }
}
```

The client switches on `code`; `message` is safe to show to the user; `details` only appears for
validation errors. FastAPI's default `{"detail": ...}` format is replaced by exception handlers
in #16.

| Status | `code` | When |
| --- | --- | --- |
| 401 | `unauthorized` | Missing, invalid or expired access token; expired or revoked refresh token |
| 401 | `invalid_credentials` | Wrong email or password on login |
| 403 | `invalid_credentials` | Wrong password when confirming account deletion. The session is still valid. |
| 404 | `not_found` | Unknown path, or a resource that doesn't exist **or belongs to another user** |
| 405 | `method_not_allowed` | Wrong HTTP method for the path |
| 409 | `conflict` | Email already registered; suggestion already accepted or rejected |
| 422 | `validation_error` | Invalid body, bad UUID in the path, or `limit`/`offset` out of range |
| 429 | `rate_limited` | Too many requests, including password attempts on register, login and account deletion (`Retry-After` header) |
| 500 | `internal_error` | Anything unexpected. No internal details are included. |
| 503 | `llm_unavailable` | The LLM failed or timed out while answering a question |

Only a 401 with `unauthorized` means the session may have expired. A wrong password never logs the
user out.

## Design decisions

- **Another user's data is a 404, not a 403.** That way nobody can find out whether an id exists.
- **Saving a note never waits for the LLM.** `POST /notes` returns at once and the client polls
  `GET /notes/{id}/suggestions`. This meets the reliability requirement that LLM failures never
  block saving, and suggestions should appear within 10 seconds.
- **Asking a question waits for the answer.** The answer must arrive within 20 seconds, so a plain
  request is simpler than polling or streaming.
- **A question is stored only when its answer succeeds.** If the LLM fails, nothing is stored and
  the client can resend the same question without creating a duplicate.
- **The client always sends `entry_date`.** The server runs in UTC, so just after midnight in
  Poland its "today" would still be the previous day.
- **Account deletion is `POST /account/delete`.** It needs the password in the body, and some
  proxies and clients drop the body of a `DELETE`.
- **The graph sends previews, not full notes.** This keeps the response small with 500 notes. The
  client loads the full note with `GET /notes/{id}` when a node is clicked.
- **Citations come back as note summaries**, not just the `cited_note_ids` stored in PostgreSQL,
  so the chat panel can show and link them without extra requests.
- **Concepts (M2) and manual links (M4) aren't included yet.** They're should-have extensions and
  will be added to this file when they're planned.

## Changes this needs elsewhere

**Data model (#10, PR #72):**
- Add `id : UUID` to `LINKED_TO`, so accept and reject can address a link.
- Add `suggestion_status : pending | ready | failed` to `Note`.
- Add a `refresh_tokens` table: `id`, `user_id` (FK → `users`, on delete cascade), `token_hash`
  (unique), `created_at`, `last_used_at`, `revoked_at` (nullable).

**Link prompt (`backend/app/prompts/prompt_links.py`):** the team agreed to keep all five link types
from section 4 of the spec, so the prompt should ask for `related`, `supports`, `contradicts`,
`extends` and `example_of`, not just three.

**Settings (#20):** the token lifetimes have to change in three files, because Docker Compose passes
its own default and overrides the one in `config.py`.

| File | `ACCESS_TOKEN_EXPIRE_MINUTES` | `REFRESH_TOKEN_IDLE_MINUTES` (new) | `COOKIE_SECURE` (new) |
| --- | --- | --- | --- |
| `backend/app/config.py` | Default 60 → 15 | Add, default 10080, must be > 0 | Add, `bool`, default `true` |
| `compose.yaml` (backend `environment`) | `${ACCESS_TOKEN_EXPIRE_MINUTES:-60}` → `:-15` | Add `${REFRESH_TOKEN_IDLE_MINUTES:-10080}` | Add `${COOKIE_SECURE:-false}` |
| `.env.example` | Comment shows 15 | Add as a commented-out line, showing 10080 | Add as a commented-out line, explaining it |

`COOKIE_SECURE` adds `Secure` to the refresh cookie. It defaults to `true` in `config.py`, so a
deployment is safe unless it opts out. Local Docker Compose sets it to `false`, because
`http://localhost` has no HTTPS.

**CORS (#16):**
- Set `allow_credentials=True`, with `allow_origins` taken from `CORS_ORIGINS`. A wildcard origin
  isn't allowed with credentials.
- Set `expose_headers=["Retry-After"]`. Otherwise the client can't read it on a 429.
- Make sure 500 responses get CORS headers, or the browser hides `internal_error` from the client. A
  handler registered with `@app.exception_handler(Exception)` runs in Starlette's
  `ServerErrorMiddleware`, which sits outside `CORSMiddleware`, so its response has no CORS headers.
  Catch unexpected exceptions in a middleware added *before* `CORSMiddleware` instead: Starlette
  wraps middleware in reverse order, so that one ends up inside CORS.

**Deployment (#58):** `SameSite=Lax` only sends the cookie when the client and the API are on the same
*site*, meaning the same registrable domain. Examples: `app.example.com` and `api.example.com`, or one
origin with a reverse proxy in front of both. Locally this holds, because `localhost:5173` and
`localhost:8000` are the same site. If they're deployed on unrelated domains, the cookie would need
`SameSite=None; Secure` and CSRF protection, so keep them on one site.
