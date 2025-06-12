# Virtual Workspace Room Booking System 🏢

A backend service to manage booking of virtual workspace rooms (Private Rooms, Shared Desks, and Conference Rooms) using Django, SQLite, and Docker.

## 📦 Tech Stack

- Python 3.12
- Django 5.x
- SQLite3
- [uv](https://github.com/astral-sh/uv) for dependency management
- Docker & Docker Compose

---

## 📁 Project Structure

```
.
├── app/
│   ├── bookings/             # Django app for room booking
│   ├── manage.py
│   ├── db.sqlite3            # SQLite DB (local only)
│   └── ...
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## 🚀 Getting Started

### 🐳 Docker Setup

#### 1. Build and Run the App

```bash
docker-compose up --build
```

This will:
- Install dependencies via `uv`
- Create a virtual environment inside the image
- Start the Django dev server on `http://localhost:8000`

---

## 🔧 API Endpoints

| Method | Endpoint                            | Description                  |
|--------|-------------------------------------|------------------------------|
| GET    | `/bookings/api/v1/rooms/`           | List all available rooms     |
| POST   | `/bookings/api/v1/create-team/`     | Create a team                |
| POST   | `/bookings/api/v1/create-room/`     | Add a room     |
| POST   | `/bookings/api/v1/bookings/`       | Book a room for user/team    |
| GET   | `/bookings/api/v1/bookings/`       | Get all room for user/team    |
| POST   | `/bookings/api/v1/cancel/<int:booking_id>/`       | Cancel a Booking     |
| POST   | `/bookings/api/v1/rooms/available/`       | Check room availability per slot     |



Example JSON payload for booking:
```json
{
  "slot": "2025-06-12T15:00:00Z",
  "room_type": "PRIVATE",
  "user": 1
}
```

---

## 🐳 Dockerfile Summary

```dockerfile
FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked
COPY . .
RUN mkdir -p data
EXPOSE 8000

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

## 🧪 Running Migrations & Superuser

```bash
docker-compose run web uv run python manage.py migrate
docker-compose run web uv run python manage.py createsuperuser
```

---

## 💡 Notes

- To persist SQLite DB, use volume: `./data:/app/data`
- Avoid volume mounts (`.:/app`) unless in development mode

---
