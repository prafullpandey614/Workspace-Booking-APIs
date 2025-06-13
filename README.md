# Virtual Workspace Room Booking System 🏢

A backend service to manage booking of virtual workspace rooms (Private Rooms, Shared Desks, and Conference Rooms) using Django, SQLite, and Docker.

## 📦 Tech Stack

- Python 3.12
- Django 5.x
- SQLite3
- [uv](https://github.com/astral-sh/uv) for dependency management
- Docker & Docker Compose



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
| POST    | `/bookings/api/v1/register/`           | Users can register themselves  |
| GET    | `/bookings/api/token/`           | Get Access Token  |
| GET    | `/bookingsapi/token/refresh/`           | Refresh JWT Token  |
| GET    | `/bookings/api/v1/rooms/`           | List all available rooms     |
| POST   | `/bookings/api/v1/create-team/`     | Create a team                |
| POST   | `/bookings/api/v1/create-room/`     | Add a room     |
| POST   | `/bookings/api/v1/bookings/`       | Book a room for user/team    |
| GET   | `/bookings/api/v1/bookings/`       | Get all room for user/team    |
| POST   | `/bookings/api/v1/cancel/<int:booking_id>/`       | Cancel a Booking     |
| POST   | `/bookings/api/v1/rooms/available/`       | Check room availability per slot     |




---
