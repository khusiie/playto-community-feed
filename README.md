# Playto Community Feed

A high-performance Community Feed prototype built with Django and React for the Playto Engineering Challenge.

## Features

- **Discussion Feed**: Create threads and view posts.
- **Threaded Comments**: Arbitrarily deep nested comments system.
- **Dynamic Leaderboard**: Real-time ranking based on Karma earned in the last 24 hours.
- **Gamification**:
  - +5 Karma for thread likes
  - +1 Karma for comment likes
- **Optimized Performance**: Solves the N+1 problem by fetching entire comment trees in a single O(1) query.

## Tech Stack

- **Backend**: Django 6.x, Django REST Framework
- **Frontend**: React, Vite
- **Database**: SQLite (Configured for easy local run, swappable for PostgreSQL)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+

### 1. Backend Setup

```bash
cd community_feed
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate
# Activate (Mac/Linux)
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create Superuser (for login)
python manage.py createsuperuser

# Run Server
python manage.py runserver
```

Backend will be running at `http://localhost:8000/api/`.

### 2. Frontend Setup

```bash
cd playto_frontend
# Install dependencies
npm install

# Run Dev Server
npm run dev
```

Frontend will be running at `http://localhost:5173`.

## Usage Note

- **Login**: Since this prototype uses Session Authentication, please log in to the Django Admin panel at **[http://localhost:8000/admin/](http://localhost:8000/admin/)** before using the frontend. This ensures your browser has the necessary session cookies.
