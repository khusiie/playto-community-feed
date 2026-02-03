# Playto Community Feed

A high-performance Community Feed prototype built with Django and React for the Playto Engineering Challenge. Optimized for high concurrency, N+1 problem resolution, and seamless user experience.

## 🚀 Live Demo

- **Frontend**: [https://playto-community-feed-frontend.onrender.com](https://playto-community-feed-frontend.onrender.com)
- **Backend API**: [https://playto-community-feed-trxe.onrender.com/api/](https://playto-community-feed-trxe.onrender.com/api/)

> [!NOTE]
> **Convenience Mode:** For this prototype, I have enabled **Guest Posting**. You can create threads, comments, and like posts immediately without logging in. All anonymous actions are automatically attributed to a "Guest" user.

## ✨ Key Features

- **Discussion Feed**: Create threads and view posts in real-time.
- **Threaded Comments**: Arbitrarily deep nested comments system.
- **Dynamic Leaderboard**: Real-time ranking based on Karma earned in the last 24 hours (updates every 2 seconds).
- **Gamification**:
  - +5 Karma for thread likes
  - +1 Karma for comment likes
- **Performance Optimized**: Uses a custom "adjacency list" deserialization strategy to solve the N+1 problem, fetching entire complex comment trees in a single O(1) database query.

## 🛠️ Tech Stack

- **Backend**: Django 6.x, Django REST Framework
- **Frontend**: React, Vite, Vanilla CSS (Custom Design)
- **Database**: PostgreSQL (Production), SQLite (Local)
- **Hosting**: Render (Automated CI/CD via GitHub)

## 📖 Technical Documentation

- **[EXPLAINER.md](EXPLAINER.md)**: Deep dive into the N+1 solution, Leaderboard logic, and AI bug fixes.
- **[walkthrough.md](file:///C:/Users/khush/.gemini/antigravity/brain/5f6b6975-5a25-4de8-9bd5-41269ed49fcd/walkthrough.md)**: Deployment logs and verification steps.

---

## 💻 Local Setup

If you wish to run the project locally:

### 1. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations & server
python manage.py migrate
python manage.py runserver
```

### 2. Frontend Setup
```bash
cd playto_frontend
npm install
npm run dev
```
