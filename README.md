# Identity Service — SFG

> Authentication and user management service. Supports Telegram Login, Google OAuth 2.0, JWT access/refresh tokens, and profile management.

---

## 📋 Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Run](#run)
- [API](#api)
- [Project Structure](#project-structure)

---

## Overview

Identity Service is the main authentication layer for the SFG platform. It handles:

- **Telegram authentication** via WebApp InitData
- **Google OAuth 2.0** for sign-in and account linking
- **JWT tokens** with access and refresh flows
- **User profiles** for reading and updating account data

Other services trust the JWT tokens issued by this service after gateway validation.

---

## Architecture

```
                    ┌─────────────────────┐
Telegram WebApp ───▶│                     │
Google OAuth    ───▶│  Identity Service   │──▶ PostgreSQL
Bot (internal)  ───▶│                     │
                    └──────────┬──────────┘
                               │ JWT tokens
                               ▼
                        API Gateway
                     (validates tokens)
```

The codebase is organized into domain, application, infrastructure, and presentation layers.

---

## Technologies

| Package | Version | Role |
|-------|--------|------|
| `fastapi[all]` | ^0.116.0 | HTTP framework |
| `sqlalchemy` | ^2.0.41 | ORM |
| `asyncpg` | ^0.30.0 | Async PostgreSQL driver |
| `alembic` | ^1.16.4 | Database migrations |
| `pyjwt` | ^2.10.1 | JWT generation and validation |
| `authlib[all]` | ^1.6.1 | OAuth 2.0 (Google) |
| `loguru` | ^0.7.3 | Logging |
| Python | ≥ 3.12 | Runtime |

---

## Run
### Local (Poetry)

```bash
cd Backend/identity-service
cp .env.example .env      # fill in all variables
poetry install
alembic upgrade head       # apply migrations
uvicorn main:app --reload --port 8002
```

### Docker

```bash
docker build -t sfg-identity-service .
docker run -p 8002:8000 --env-file .env sfg-identity-service
```

> **Dependencies**: PostgreSQL. Google OAuth requires valid `client_id` and `client_secret` values.

---
## API

### `GET /health`

```json
{ "status": "ok", "service": "identity-service" }
```

### Auth — `/auth`

| Method | Path | Description |
|-------|------|----------|
| `POST` | `/auth/telegram` | Authenticate with Telegram WebApp InitData |
| `POST` | `/auth/refresh` | Refresh the access token |
| `POST` | `/auth/logout` | Log out and clear the refresh token |
| `GET` | `/auth/google` | Redirect to Google OAuth |
| `GET` | `/auth/callback/google` | Google OAuth callback |

### Profile — `/profile`

| Method | Path | Description |
|-------|------|----------|
| `GET` | `/profile/me` | Get the current user profile |
| `PATCH` | `/profile/me` | Update the current user profile |

---

## Project Structure

```
identity-service/
├── main.py                    # FastAPI entry point and middleware
├── app/
│   ├── domain/                # Entities and protocols
│   ├── application/           # Use cases
│   ├── infrastructure/
│   │   ├── database/          # SQLAlchemy engine and base
│   │   └── di.py              # Dependency injection
│   └── presentation/
│       ├── api/v1/
│       │   ├── auth_user_controller.py
│       │   ├── profile_controller.py
│       │   ├── link_google_controller.py
│       │   └── internal_controller.py
│       └── middleware/
│           ├── cors.py
│           └── session.py
├── alembic/                   # Database migrations
├── Dockerfile
└── pyproject.toml
```
