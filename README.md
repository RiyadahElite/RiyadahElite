# Riyadah Elite - Full-Stack Gaming Platform

A comprehensive gaming platform built with React (Vite + Tailwind) frontend and Django backend, integrated with Supabase for data persistence.

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite for fast development
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls

### Backend
- Django 5.1.3
- Django REST Framework
- django-cors-headers
- Session-based authentication
- SQLite3 database

### Database
- Supabase (PostgreSQL)
- Row Level Security (RLS) enabled
- Tables: profiles, tournaments, tournament_participants

## Project Structure

```
.
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── context/      # React context (Auth)
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── types/        # TypeScript types
│   └── package.json
│
├── backend/              # Django backend
│   ├── settings.py      # Django settings
│   └── urls.py          # URL routing
│
├── authapp/             # Authentication app
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   └── urls.py          # Auth routes
│
├── requirements.txt     # Python dependencies
├── manage.py           # Django management
└── start-backend.sh    # Backend startup script
```

## Getting Started

### Prerequisites
- Python 3.13+
- Node.js 18+
- npm or pnpm

### Backend Setup

1. Install Python dependencies:
```bash
python3 -m pip install --user -r requirements.txt
```

2. Run Django migrations:
```bash
python3 manage.py migrate
```

3. Start the Django development server:
```bash
python3 manage.py runserver 127.0.0.1:8000
```

Or use the convenience script:
```bash
./start-backend.sh
```

The backend API will be available at `http://127.0.0.1:8000/api/`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Authentication (`/api/auth/`)
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/user/` - Get current user

### Request Examples

**Register:**
```json
POST /api/auth/register/
{
  "username": "player1",
  "email": "player1@example.com",
  "password": "securepass123",
  "password2": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Login:**
```json
POST /api/auth/login/
{
  "username": "player1",
  "password": "securepass123"
}
```

## Database Schema

### Profiles Table
- `id` (uuid, primary key)
- `username` (text, unique)
- `email` (text)
- `first_name` (text)
- `last_name` (text)
- `role` (text, default: 'player')
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

### Tournaments Table
- `id` (uuid, primary key)
- `title` (text)
- `description` (text)
- `game` (text)
- `start_date` (timestamptz)
- `prize_pool` (numeric)
- `status` (text, default: 'upcoming')
- `created_at` (timestamptz)

### Tournament Participants Table
- `id` (uuid, primary key)
- `tournament_id` (uuid, references tournaments)
- `user_id` (uuid, references profiles)
- `registered_at` (timestamptz)

## Features

- User authentication (register, login, logout)
- Session-based auth with Django
- Protected routes in React
- Tournament browsing
- User dashboards (Player, Host, Admin, Moderator)
- Game testing submission
- Community features
- Rewards system
- Contact form

## Development

### Running Both Servers

You need to run both the Django backend and React frontend simultaneously:

**Terminal 1 (Backend):**
```bash
./start-backend.sh
```

**Terminal 2 (Frontend):**
```bash
cd frontend && npm run dev
```

### CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:5173`
- `http://127.0.0.1:5173`

CORS credentials are enabled for session authentication.

## Deployment

### Backend Deployment
- Set `DEBUG = False` in `settings.py`
- Configure `ALLOWED_HOSTS`
- Use production database
- Set secure `SECRET_KEY`
- Configure static files serving

### Frontend Deployment
- Build the frontend: `npm run build`
- Serve the `dist` folder
- Update `VITE_API_URL` environment variable

## Security Features

- Row Level Security (RLS) on all Supabase tables
- Session-based authentication
- CSRF protection
- Password validation
- Secure HTTP-only cookies

## License

MIT License
