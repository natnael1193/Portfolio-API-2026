# portfolio-api

FastAPI backend for the portfolio site. Provides REST endpoints for projects, posts,
skills, experience, contact messages, page views, and a streaming AI chat.

## Stack

- **FastAPI** — API framework
- **PostgreSQL** — database
- **SQLAlchemy 2** — ORM
- **Alembic** — migrations
- **Pydantic v2** — validation and settings
- **python-jose** — JWT auth
- **Anthropic SDK** — AI chat streaming
- **Resend** — transactional email

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # fill in your values
```

## Database

```bash
# Run migrations
alembic upgrade head

# Create a new migration after model changes
alembic revision --autogenerate -m "describe your change"
```

## Development

```bash
uvicorn app.main:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs (only when DEBUG=true)
```

## First admin account

After running migrations, register your admin via:

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "yourpassword", "full_name": "Your Name"}'
```

This endpoint is permanently disabled once any admin exists.

## Docker

```bash
docker build -t portfolio-api .
docker run -p 8000:8000 --env-file .env portfolio-api
```

## Deploy (Railway)

1. Push to GitHub
2. New project → Deploy from repo
3. Add environment variables from `.env.example`
4. Railway auto-detects the Dockerfile

## API routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /api/auth/register | — | First-time admin setup |
| POST | /api/auth/token | — | Login → JWT |
| GET | /api/auth/me | Admin | Current admin info |
| GET | /api/projects | — | List published projects |
| GET | /api/projects/{slug} | — | Single project |
| POST | /api/projects | Admin | Create project |
| PATCH | /api/projects/{id} | Admin | Update project |
| DELETE | /api/projects/{id} | Admin | Delete project |
| GET | /api/projects/admin/all | Admin | All projects incl. drafts |
| GET | /api/posts | — | List published posts |
| GET | /api/posts/{slug} | — | Single post |
| POST | /api/posts | Admin | Create post |
| PATCH | /api/posts/{id} | Admin | Update post |
| DELETE | /api/posts/{id} | Admin | Delete post |
| GET | /api/skills | — | List all skills |
| POST | /api/skills | Admin | Create skill |
| PATCH | /api/skills/{id} | Admin | Update skill |
| DELETE | /api/skills/{id} | Admin | Delete skill |
| GET | /api/experience | — | List experience |
| POST | /api/experience | Admin | Create entry |
| PATCH | /api/experience/{id} | Admin | Update entry |
| DELETE | /api/experience/{id} | Admin | Delete entry |
| POST | /api/contact | — | Submit contact form |
| GET | /api/contact | Admin | List messages |
| PATCH | /api/contact/{id}/read | Admin | Mark as read |
| DELETE | /api/contact/{id} | Admin | Delete message |
| GET | /api/views | — | Get page view count |
| POST | /api/views | — | Increment page views |
| POST | /api/chat | — | Streaming AI chat |
| GET | /health | — | Health check |
