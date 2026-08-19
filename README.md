# Finance Tracker

A personal income and expense tracker, written twice: once as a Python CLI over
raw SQLite, and once as a FastAPI + SQLAlchemy REST API.

**Early and experimental.** It was written to work through the same problem at
two levels of abstraction — hand-written SQL and cursor management on one side,
an ORM with request validation on the other. It is not a finished product and
has no frontend.

## The two halves

### `cli/` — Python + sqlite3

A menu-driven terminal program. Creates the `transactions` table on first run,
validates dates and amounts before touching the database, and recovers from a
missing or corrupted file rather than crashing.

```bash
python cli/main.py
```

### `web/` — FastAPI + SQLAlchemy

A REST API over the same data model, with Pydantic schemas separating what
comes in from what goes out.

```bash
uvicorn web.main:app --reload
```

| Method | Path | Does |
|---|---|---|
| `POST` | `/transactions` | Create a transaction |
| `GET` | `/transactions` | List all |
| `GET` | `/transactions/{id}` | Fetch one |
| `PATCH` | `/transactions/{id}` | Update |
| `DELETE` | `/transactions/{id}` | Delete |

Validation is enforced at the boundary: `t_type` must be `income` or `expense`,
and `amount` must be positive — a bad request gets a 400, not a bad row.

Interactive docs at `/docs` once it is running.

## Data model

| Field | Type |
|---|---|
| `id` | integer, primary key |
| `amount` | float, positive |
| `t_type` | `income` \| `expense` |
| `category` | string |
| `date` | `YYYY-MM-DD` |
| `description` | string, optional |
| `created_at` | timestamp |

## Known limitations

- The CLI and the API do not share a database file or a schema definition.
- No authentication — the API is single-user and assumes localhost.
- No reporting, aggregation, or category summaries yet.
