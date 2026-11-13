# Diagrams

Design diagrams for deliverable D3. Each diagram is a [PlantUML](https://plantuml.com) source
file (`.puml`) with exported `.svg` and `.png` images next to it. Edit the source, then
re-render. Don't edit the images by hand.

```bash
scripts/render-diagrams.sh                 # all diagrams (needs Docker)
scripts/render-diagrams.sh use-case.puml   # just one
```

Commit the source and both images together. For live preview while editing, use the
PlantUML extension for VS Code or JetBrains.

| Diagram | Source | Issue |
| --- | --- | --- |
| Use-case diagram | [use-case.puml](use-case.puml) | #8 |
| Component diagram | [component.puml](component.puml) | #9 |

## Use-case diagram

![Use-case diagram](use-case.svg)

### Actors

| Actor | Description |
| --- | --- |
| Visitor | Someone without a session: not registered yet, or logged out |
| Registered user | A logged-in user working with their own private notes |
| LLM provider | External LLM API (OpenAI or Anthropic) behind the intelligence layer |

### Requirement traceability

Every high-priority requirement from the specification maps to at least one use case.

| Requirement | Use cases |
| --- | --- |
| H1 Register and log in | Register, Log in, Log out |
| H2 Create, edit and delete notes | Browse daily notes, Create note, Edit note, Delete note, Open note |
| H3 Suggest links | Generate link suggestions (included in Create note and Edit note) |
| H4 Accept or reject links | Review link suggestions, Accept link, Reject link |
| H5 Interactive graph | Explore knowledge graph, Open note |
| H6 Ask questions with citations | Ask a question, Open note (a cited note) |
| Privacy (non-functional) | Export all data, Delete account |

Medium- and low-priority extensions (M1–M5, L1–L5) are left out until they are planned.

## Component diagram

![Component diagram](component.svg)

The six components match the architecture in section 3 of the specification. In UML 2.5
notation, a solid line to a circle means the component *provides* that interface, and a
dashed «use» arrow means it *requires* it.

### Interfaces

| Interface | Provided by | Used by | Purpose |
| --- | --- | --- | --- |
| Nodebook REST API | FastAPI backend | React client | All client traffic: JSON over HTTPS, authenticated with a JWT. Documented by the generated OpenAPI schema |
| Link suggestion | Intelligence layer | FastAPI backend | Embed a saved note and propose up to 5 links with score, type and reason. Runs in the background and is retried on failure |
| Question answering | Intelligence layer | FastAPI backend | Answer a question from the user's notes and return the cited note ids |
| Bolt / Cypher | Neo4j | FastAPI backend, intelligence layer | Graph reads and writes, plus vector search. The query agent's tools read Neo4j directly |
| SQL | PostgreSQL | FastAPI backend | Accounts, chat sessions and chat messages |
| LLM completion API | External LLM API | Intelligence layer | Prompts for link reasoning, concept extraction and answers, sent through a single swappable LLM client |

Only the intelligence layer talks to the LLM, and only the backend is reachable from the
client. Concept extraction belongs to extension M2.
