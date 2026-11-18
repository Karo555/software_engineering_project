# Contributing to Nodebook

This guide covers how the team plans, branches, commits, reviews and merges work.
If something here gets in the way, open an issue and suggest a change.

## Planning

- Every piece of work starts as a GitHub issue. If there is no issue, create one first.
- Issues are grouped into milestones that match the course deliverables (D2–D8),
  plus the *Extensions (should have)* and *Backlog (could have)* milestones.
- Each issue has one `type:` label, one `priority:` label and at least one `area:` label.

| Label group | Values |
| --- | --- |
| `type:` | `feature` (user-facing), `task` (technical or setup), `docs`, `test` |
| `priority:` | `high` (must have), `medium` (should have), `low` (could have) |
| `area:` | `backend`, `frontend`, `ai`, `data`, `devops` |

### Project board

Issues are tracked on the [project board](https://github.com/users/Karo555/projects/4).

| Column | Meaning |
| --- | --- |
| Backlog | Not yet planned, or still blocked by another issue |
| Ready | Dependencies are done and the work can start |
| In progress | Someone is assigned and working on it on a branch |
| In review | A pull request is open and waiting for review |
| Done | Merged and meets the [Definition of Done](#definition-of-done) |

Move your own cards as you go. Before you start an issue, check its **Depends on** line.
Only take work from *Ready* unless you have agreed otherwise with the project manager.

## Branches

`main` is always in a working state. Nobody pushes to it directly; all changes arrive
through pull requests.

Create one short-lived branch per issue, named `<type>/<issue-number>-<short-description>`:

| Prefix | Use for |
| --- | --- |
| `feat/` | User-facing features (`type: feature`) |
| `fix/` | Bug fixes |
| `docs/` | Documentation and diagrams |
| `test/` | Tests only |
| `chore/` | Setup, tooling, dependencies, CI, Docker |

Examples: `feat/19-user-registration`, `chore/5-docker-compose`, `docs/8-use-case-diagram`.

Keep branches small and merge often. If a branch has been open for more than a few
days, consider splitting the issue.
Rebase on `main` (or merge `main` into your branch) before asking for review.

## Commits

- Write the subject line in the imperative mood, start it with a capital letter,
  and don't end it with a full stop: *Add note CRUD endpoints*, not *added endpoints.*
- Keep the subject under about 72 characters. Use the body, after a blank line,
  to explain *why* when it isn't obvious.
- Make each commit one logical change. Don't mix formatting with behaviour changes.
- Never commit secrets, `.env` files, API keys or database dumps.

## Pull requests

1. Open a pull request into `main` and fill in the template.
2. Link the issue in the description with `Closes #<number>`, so it closes on merge.
3. Use a draft pull request for early feedback; mark it *Ready for review* when it is done.
4. Request a review from at least one teammate, preferably the owner of the affected area.

### Review rules

- At least **one approval** from someone other than the author is needed before merging.
- CI must pass. A failing check is never merged "to fix later".
- Reviewers aim to respond within **two working days**. If you can't, say so
  so the author can ask someone else.
- Reviewers check correctness, tests, readability and the acceptance criteria.
  Comments starting with **nit:** are optional suggestions; others need an answer.
- The author resolves review comments and merges. Use **Squash and merge**
  so each issue lands on `main` as a single commit, then delete the branch.

## Definition of Done

An issue is done when all of the following are true:

- [ ] Every acceptance criterion in the issue is met and ticked off.
- [ ] The change is merged into `main` through a reviewed pull request.
- [ ] CI is green: linting, formatting and all tests pass.
- [ ] New or changed behaviour has automated tests. Backend line coverage stays at or above 70%.
- [ ] New API endpoints have request and response models and appear correctly in the OpenAPI schema.
- [ ] Every new Neo4j or PostgreSQL query that reads user data is filtered by `user_id`.
- [ ] UI changes work with the keyboard alone and at widths from tablet to 1280 px desktop.
- [ ] No secrets are in the code; any new environment variable is added to `.env.example`.
- [ ] The system still starts from a clean checkout with `docker compose up`.
- [ ] README, `docs/` and diagrams are updated if setup, behaviour or architecture changed.
- [ ] The issue is closed and its card is in *Done* on the board.

Items that don't apply to an issue (for example, API checks on a documentation change)
can be skipped. Say so in the pull request.
