# ConnectHub

ConnectHub is a full-stack social networking application built with React and Django REST Framework. It lets people create profiles, connect with other users, share posts, and interact through a social feed.

## Live Demo

- Frontend: [ConnectHub](https://connect-hub-pink-two.vercel.app/)
- Backend API: [ConnectHub API](https://connecthub-backend-3k3t.onrender.com/)
- API health check: [GET /api/hello/](https://connecthub-backend-3k3t.onrender.com/api/hello/)

## Tech Stack

- **Frontend:** React, Vite, JavaScript
- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL in production; SQLite for local development
- **Deployment:** Vercel (frontend), Render (backend)

## Features

- User registration and login/logout
- Session authentication with CSRF protection
- User profiles and user search
- Follow and unfollow users
- Social feed
- Create posts with image uploads
- Like posts and add comments
- Notifications
- REST API with centralized frontend API request handling

## Architecture

```text
React + Vite frontend on Vercel
        ↓ HTTPS / REST API
Django REST Framework backend on Render
        ↓ Django ORM
PostgreSQL production database
```

The frontend sends API requests to the backend over HTTPS. Django applies authentication and permission checks, accesses application data through Django ORM, and returns responses to the frontend. PostgreSQL stores production application data.

## Security & Authentication

- Authentication uses Django sessions.
- The frontend obtains and sends CSRF tokens for protected requests using the `X-CSRFToken` header.
- The centralized frontend API helper includes `credentials: "include"` so browser requests carry session cookies.
- Cross-origin access is configured with CORS settings, and the frontend origin is included in the backend's CSRF trusted origins.
- Secrets and deployment-specific settings are provided through environment variables and should not be committed.
- Production runs with `DEBUG=False` and secure cross-site cookie settings for the separately hosted frontend and backend.

## Backend & API

The backend uses Django and Django REST Framework. Django models represent users, profiles, follows, posts, likes, comments, and notifications. The API provides:

- Authentication and session handling
- Profile and user data
- Follow relationships
- Posts and image uploads
- Likes and comments
- Notifications and user search
- Request validation and API responses

Django ORM handles database access. SQLite is used for local development, while PostgreSQL is used in production. The health endpoint is `GET /api/hello/`.

Example response:

```json
{
  "message": "connecthub"
}
```

## Local Development

### Prerequisites

- Python 3.10+
- Node.js and npm
- Git

Clone the repository:

```bash
git clone https://github.com/RishavAry/ConnectHub.git
cd ConnectHub
```

### Backend

From the repository root, create and activate a virtual environment, install dependencies, apply migrations, and start Django:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Configure the required local environment variables before running the backend. Keep secrets out of the repository and do not commit them.

### Frontend

In another terminal, set the API base URL and start the Vite development server:

```bash
cd frontend
npm install
npm run dev
```

Set the frontend API base URL to `http://127.0.0.1:8000` with the `VITE_API_BASE_URL` environment variable. SQLite is used locally; PostgreSQL is used in production.

## Demo

- [Live frontend](https://connect-hub-pink-two.vercel.app/)
- [Backend API](https://connecthub-backend-3k3t.onrender.com/)
- [API health endpoint](https://connecthub-backend-3k3t.onrender.com/api/hello/)

## Screenshots

### Login

![ConnectHub login screen](docs/screenshots/login.png)

### Feed

![ConnectHub social feed](docs/screenshots/feed.png)

### Create a post

![ConnectHub create post screen](docs/screenshots/create-post.png)

### Profile

![ConnectHub profile screen](docs/screenshots/profile.png)

### Notifications

![ConnectHub notifications screen](docs/screenshots/Notification.png)

## Project Structure

```text
ConnectHub/
├── accounts/
├── config/
├── frontend/
├── docs/
│   └── screenshots/
├── manage.py
├── requirements.txt
└── README.md
```

## Project Status

ConnectHub is deployed and demonstrates its core authentication, social networking, posts, interactions, search, and notification functionality. Image uploads are implemented. Persistent production media storage is unfinished.

## Future Improvements

- Finish persistent production media storage
- Add automated testing
- Improve API documentation
- Add background task processing
- Add caching and performance improvements
- Add Docker/containerization
- Add CI/CD
- Add moderation and platform-management features
