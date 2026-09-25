cat > README.md <<'EOF'
# ConnectHub

ConnectHub is a full-stack social networking application built with React, Django REST Framework, and PostgreSQL.

The project provides user authentication, profiles, following, posts, image uploads, likes, comments, search, and notifications through a REST API-backed web application.

## Live Demo

- Frontend: https://connect-hub-pink-two.vercel.app/
- Backend API: https://connecthub-backend-3k3t.onrender.com/
- API Health Check: https://connecthub-backend-3k3t.onrender.com/api/hello/

## Tech Stack

### Frontend
- React
- Vite
- JavaScript

### Backend
- Python
- Django
- Django REST Framework

### Database
- PostgreSQL

### Deployment
- Vercel
- Render


## Features

### Authentication
- User registration
- Login and logout
- Session-based authentication
- CSRF-protected state-changing requests

### User Profiles
- User profiles
- Profile information
- Profile navigation
- User search

### Social Features
- Follow and unfollow users
- View other users
- Social feed

### Posts
- Create posts
- Upload images with posts
- View posts in the feed
- Like and unlike posts
- Add comments

### Notifications
- Notifications for social interactions and activity

### API
- REST API built with Django REST Framework
- Centralized frontend API request handling
- JSON-based API communication


## Architecture

ConnectHub follows a client-server architecture:

![ConnectHub Architecture](docs/architecture.png)

### Request Flow

1. The React frontend sends HTTPS requests to the Django REST API.
2. Django REST Framework handles authentication, validation, and application logic.
3. Django ORM communicates with PostgreSQL.
4. The backend returns API responses to the React frontend.


## Security & Authentication

ConnectHub uses session-based authentication with CSRF protection for state-changing requests.

### Authentication
- User registration and login
- Session-based authentication
- Protected endpoints for authenticated users
- Logout and session handling

### CSRF Protection
- CSRF tokens are fetched from the backend
- Frontend requests send the `X-CSRFToken` header
- Credentials are included with API requests
- Multipart `FormData` requests are handled without manually overriding the browser's `Content-Type`
- API requests are centralized through the frontend API helper

### Cross-Origin Configuration
Because the frontend and backend are deployed separately, production CORS and CSRF trusted origins are configured for the deployed frontend.

### Environment Configuration
Sensitive configuration is stored through environment variables rather than committed to the repository.

Production configuration includes:
- Django secret key
- Database connection
- Allowed hosts
- CORS origins
- CSRF trusted origins

### Production Security
- `DEBUG=False` in production
- Secrets are excluded from Git
- Production cookies use secure cross-site settings
EOF
## Backend & API

The backend is built with Django and Django REST Framework and provides the application API used by the React frontend.

### Core Backend Components

The application includes backend models for:

- Users
- Profiles
- Follows
- Posts
- Likes
- Comments
- Notifications

### API Responsibilities

The backend handles:

- User authentication and session management
- User and profile data
- Follow relationships
- Post creation and retrieval
- Image uploads
- Likes and comments
- Notifications
- Search and user discovery
- Request validation and API responses

### Database

Django ORM is used to communicate with the PostgreSQL production database.

The database stores the application's users, profiles, social relationships, posts, interactions, and notifications.

### API Health Check

A health endpoint is available at:

`GET /api/hello/`

Example response:

```json
{
  "message": "connecthub"
}


## Local Development

### Prerequisites

Make sure the following are installed:

- Python 3.10+
- Node.js
- npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/RishavAry/ConnectHub
cd connecthub


## Demo

### Live Application

[Open ConnectHub](https://connect-hub-pink-two.vercel.app/)

### Backend API

[ConnectHub API](https://connecthub-backend-3k3t.onrender.com/)

### API Health Check

[Health Check](https://connecthub-backend-3k3t.onrender.com/api/hello/)

## Screenshots

Screenshots showcasing the main parts of the application:

### Login

![ConnectHub Login](docs/screenshots/login.png)

### Home Feed

![ConnectHub Feed](docs/screenshots/feed.png)

### Create Post

![Create Post](docs/screenshots/create-post.png)

### Profile

![ConnectHub Profile](docs/screenshots/profile.png)

### Notifications

![ConnectHub Notifications](docs/screenshots/notifications.png)

## Project Structure

```text
connecthub/
├── accounts/            # Django application: models, views, serializers, auth
├── config/              # Django project configuration and settings
├── frontend/            # React + Vite frontend
├── docs/
│   └── screenshots/     # Project screenshots
├── manage.py
├── requirements.txt
└── README.md
