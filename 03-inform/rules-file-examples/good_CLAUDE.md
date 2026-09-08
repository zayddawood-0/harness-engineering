# Project rules — `orders-api`

## Stack

- Python 3.11, FastAPI, PostgreSQL via SQLAlchemy 2.0 (async engine).
- Tests: `pytest tests/ -x` must pass before any commit. Run `ruff check .` for lint.

## Database

- Never write a migration that drops a column in the same PR that stops using it. Deploy the "stop using it" change first, ship it, THEN drop the column in a follow-up PR. This repo has had two incidents from combining these.
- All new tables need a `created_at TIMESTAMPTZ DEFAULT now()` column — the analytics pipeline in `reporting/` assumes every table has one.
- Migrations live in `migrations/` and are named `NNNN_description.sql`, zero-padded to 4 digits. Check the latest number in the folder before creating a new one — do not guess based on git log.

## API conventions

- Every new endpoint needs a Pydantic response model, even for simple returns. See `app/routes/orders.py` for the pattern to copy.
- Error responses use the shared `AppError` class in `app/errors.py`, not raw `HTTPException` — it's what wires into our error tracking.
- Do not add new query parameters to `GET /orders` without checking `app/routes/orders.py` line ~40 — there's an existing filter dispatch table that new params must be registered in, or they'll be silently ignored.

## Testing

- Integration tests hit a real test database (`docker compose up -d test-db`), not mocks — we've had mocked tests pass while the real migration broke prod. See `HARNESS.md` if this repo has one.
- If you add a new external API call, add a recorded fixture in `tests/fixtures/` using `vcr.py` — do not let tests make live network calls.

## Before committing

1. `ruff check .`
2. `pytest tests/ -x`
3. `git diff` — confirm no debug prints, no commented-out code, no `.env` values pasted into a file by accident.
