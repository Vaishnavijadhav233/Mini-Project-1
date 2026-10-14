# Mini-Project-1
Library Management Platform
===========================

A Flask + SQLite app for running a small library: catalogue search, member
management, issue / return / renew, automatic late fines, and a librarian dashboard.

Features
--------
- Public catalogue with search (title, author, ISBN, category) and status filter
- Librarian login (session based, CSRF-protected forms)
- Add / delete books, add / delete members
- Issue books to members (14-day loan), renew, return
- Late fine of Rs 5 per day, calculated on return
- Dashboard: totals, overdue list with running fines, recent activity
- JSON API: `GET /api/books?q=...`, health check: `GET /health`
- Existing databases are migrated automatically (old `books.due` data is kept)

Run locally
-----------
    pip install -r requirements.txt
    $env:DATABASE="library.db"; $env:ADMIN_PASSWORD="secret"; python -m flask --app app run
    python -m pytest

Deploy with Docker
------------------
    copy .env.example .env      # then edit SECRET_KEY and ADMIN_PASSWORD
    docker compose up -d --build

The app listens on http://localhost:8000 and stores data in the `library-data` volume.
For production put it behind an HTTPS reverse proxy and set `COOKIE_SECURE=1`.
Platforms like Render, Railway or Fly.io can use the Dockerfile directly: set
`SECRET_KEY`, `ADMIN_PASSWORD`, mount a persistent disk at `/data`, and use `/health`
as the health check. Run a single instance (SQLite).

Configuration (environment variables)
-------------------------------------
| Name | Default | Purpose |
|------|---------|---------|
| SECRET_KEY | random per start | Session signing key (set it so logins survive restarts) |
| ADMIN_USER | admin | Librarian username |
| ADMIN_PASSWORD | random, logged at start | Librarian password |
| DATABASE | /data/library.db | SQLite file path |
| PORT | 8000 | Listen port (Docker) |
| COOKIE_SECURE | 0 | Set 1 behind HTTPS |
