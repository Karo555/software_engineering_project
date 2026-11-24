# REST API contract

[openapi.yaml](openapi.yaml) is the draft contract between the React client and the FastAPI
backend (issue #14). The backend, the frontend and the intelligence layer all build against it.

Once the endpoints exist, FastAPI generates the live schema at `/openapi.json` and the docs at
`/docs`. If the code and this file disagree, fix whichever is wrong in the same pull request.

**Viewing it:** paste the file into [editor.swagger.io](https://editor.swagger.io), or open it
in VS Code with the *OpenAPI (Swagger) Editor* extension.

## Endpoints

All paths are under `/api/v1`. Everything except register and login needs `Authorization: Bearer <token>`.

| Requirement | Method and path | What it does |
| --- | --- | --- |
| H1 | `POST /auth/register` | Create an account (password at least 8 characters) |
| H1 | `POST /auth/login` | Get a JWT access token |
| H1 | `POST /auth/logout` | Log out (the client discards the token) |
| H1 | `GET /auth/me` | The logged-in user |
| H2 | `GET /notes` | List notes, newest entry date first, filterable by `from` and `to` |
| H2 | `POST /notes` | Create a note; suggestions start in the background |
| H2 | `GET /notes/{id}` | A note with its accepted links |
| H2 | `PATCH /notes/{id}` | Edit a note; new suggestions start if the content changed |
| H2 | `DELETE /notes/{id}` | Delete a note and its links |
| H3 | `GET /notes/{id}/suggestions` | Suggestion job status (`pending`, `ready`, `failed`) and up to 5 suggestions |
| H4 | `GET /suggestions` | Review queue: all pending suggestions, best first |
| H4 | `POST /suggestions/{id}/accept` | Accept a link; it appears in the graph |
| H4 | `POST /suggestions/{id}/reject` | Reject a link; the pair is never suggested again |
| H5 | `GET /graph` | Notes (with a short preview) and accepted links, filterable by date |
| H6 | `GET`, `POST /chat/sessions` | List or start chat sessions |
| H6 | `GET`, `DELETE /chat/sessions/{id}` | A session with its messages, or delete it |
| H6 | `POST /chat/sessions/{id}/messages` | Ask a question; returns the answer with cited notes |
| Privacy | `GET /account/export` | Download all of the user's data as JSON |
| Privacy | `DELETE /account` | Delete the account and all data (password needed again) |

`GET /health` stays at the root, outside `/api/v1`, for Docker health checks.

## Errors

Every error, including validation errors, has the same shape:

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
| 401 | `unauthorized` | Missing, invalid or expired token; wrong email or password |
| 404 | `not_found` | Doesn't exist, **or belongs to another user** |
| 409 | `conflict` | Email already registered; suggestion already accepted or rejected |
| 422 | `validation_error` | Invalid body or parameters |
| 429 | `rate_limited` | Too many requests (`Retry-After` header) |
| 503 | `llm_unavailable` | The LLM failed or timed out while answering a question |
| 500 | `internal_error` | Anything unexpected |

## Design decisions

- **Another user's data is a 404, not a 403.** That way nobody can find out whether an id exists.
- **Saving a note never waits for the LLM.** `POST /notes` returns at once and the client polls
  `GET /notes/{id}/suggestions`. This meets the reliability requirement that LLM failures never
  block saving, and suggestions should appear within 10 seconds.
- **Asking a question waits for the answer.** The answer must arrive within 20 seconds, so a plain
  request is simpler than polling or streaming. Streaming can be added later without changing
  the stored messages.
- **Logout is client-side.** Tokens are stateless JWTs that expire after 60 minutes. Revoking
  them on the server would need a denylist table that isn't in the data model.
- **The graph sends previews, not full notes.** This keeps the response small with 500 notes. The
  client loads the full note with `GET /notes/{id}` when a node is clicked.
- **Citations come back as note summaries**, not just the `cited_note_ids` stored in PostgreSQL,
  so the chat panel can show and link them without extra requests.
- **Concepts (M2) and manual links (M4) aren't included yet.** They're should-have extensions and
  will be added to this file when they're planned.

## Open questions

- **Links need an `id`.** Accept and reject address a link by id, but `LINKED_TO` in the data
  model (#10) has no `id` property. Proposal: add `id : UUID` to `LINKED_TO`, created with the
  suggestion.
- **Link types:** the data model has five (`related`, `supports`, `contradicts`, `extends`,
  `example_of`), but the link prompt in `backend/app/prompts/prompt_links.py` only asks the LLM
  for three (`related`, `contradicts`, `extends`). The API accepts all five. Should the prompt
  use all five, or should the data model drop two?
