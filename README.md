# Nodebook

Nodebook is a web application that turns daily notes into a personal knowledge graph.
It suggests links between notes, the user accepts or rejects them, and a query agent
answers questions about the graph with citations to the source notes.

Software Engineering course project, Wrocław University of Science and Technology, 2026/27.

## Repository structure

| Folder | Contents |
| --- | --- |
| `backend/` | Python 3.12, FastAPI, Neo4j, PostgreSQL |
| `frontend/` | TypeScript, React, Vite |
| `docs/` | Specification, diagrams, reports |
| `scripts/` | Project tooling (GitHub issue import) |

## Setup

You need [Docker](https://docs.docker.com/get-docker/) with Compose v2.

```bash
cp .env.example .env   # then replace the placeholder passwords
docker compose up      # add --build after changing a Dockerfile or dependencies
```

| Service | URL |
| --- | --- |
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 (health check at `/health`) |
| Neo4j Browser | http://localhost:7474 (user `neo4j`, password from `.env`) |
| PostgreSQL | `localhost:5432` |

Code in `backend/` and `frontend/` is mounted into the containers and reloads on save.
Database data is kept in named volumes. `docker compose down` keeps it, and
`docker compose down -v` deletes it.

If a port is already in use on your machine, override it in `.env`
(see the optional port settings in `.env.example`).

## Team

| Role | Member |
| --- | --- |
| Project manager | Karo555 |
| Frontend developer | kanwa5000|
| Backend developer | Aktreides44 |
| AI engineer | emiliamykowska|
| Data and QA engineer | majano-pwr |

## Licence

MIT, see [LICENSE](LICENSE).
