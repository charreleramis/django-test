# Django Ride Management API

A Django REST Framework API for managing rides, users, and ride events with authentication and admin role-based access control.

## Prerequisites

- Python 3.14 (or compatible version)
- pipenv (Python package manager)
- Git

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd django-test
```

### 2. Install dependencies using pipenv

```bash
# Install pipenv if you don't have it
pip install pipenv

# Install project dependencies
pipenv install
```

This will install:
- Django 6.0.2
- Django REST Framework

### 3. Navigate to the project directory

```bash
cd todo_project
```

### 4. Run database migrations

```bash
python manage.py migrate
```

This will create the SQLite database and set up all necessary tables.

## Running the Application

### 1. Activate the pipenv shell

```bash
pipenv shell
```

### 2. Start the development server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## Seeding Data

To populate the database with sample data (rides, users, and ride events):

```bash
python manage.py seed_data
```

This command will create:
- Sample users (admins, drivers, riders)
- Sample rides with various statuses
- Sample ride events associated with rides

## API Endpoints

### Base URL
All API endpoints are prefixed with `/api/`

### Authentication

**Note:** All API endpoints (except signin/signup) require admin role authentication.

#### Sign Up
- **POST** `/api/users/signup/`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "role": "admin"
  }
  ```
- **Response:** Returns user data and authentication token (set as cookie)

#### Sign In
- **POST** `/api/users/signin/`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response:** Returns user data and authentication token (set as cookie)

**Authentication Methods:**
- Cookie-based: Token is automatically set in `auth_token` cookie after signin/signup
- Header-based: Include `Authorization: Token <token>` in request headers

### User Endpoints

- **GET** `/api/users/` - List all users (admin only, paginated)
- **GET** `/api/users/{id_user}/` - Retrieve a specific user (admin only)
- **POST** `/api/users/` - Create a new user (admin only)
- **PUT/PATCH** `/api/users/{id_user}/` - Update a user (admin only)
- **DELETE** `/api/users/{id_user}/` - Delete a user (admin only)

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10)

### Ride Endpoints

#### List Rides
- **GET** `/api/rides/`
- **Query Parameters:**
  - `page` - Page number (default: 1)
  - `page_size` - Items per page (default: 10)
  - `status` - Filter by ride status (`en-route`, `pickup`, `dropoff`, `completed`, `cancelled`)
  - `email` - Filter by rider email (partial match)
  - `sort` - Sort by `pickup_time`, `-pickup_time`, `distance`, or `-distance`
  - `lat` - Latitude for distance sorting (required with `sort=distance`)
  - `lon` - Longitude for distance sorting (required with `sort=distance`)

**Examples:**
```bash
# Get paginated rides
GET /api/rides/?page=1&page_size=10

# Filter by status
GET /api/rides/?status=completed

# Filter by rider email
GET /api/rides/?email=user@example.com

# Sort by pickup time (ascending)
GET /api/rides/?sort=pickup_time

# Sort by pickup time (descending)
GET /api/rides/?sort=-pickup_time

# Sort by distance from GPS coordinates
GET /api/rides/?sort=distance&lat=40.7128&lon=-74.0060

# Sort by distance (descending)
GET /api/rides/?sort=-distance&lat=40.7128&lon=-74.0060
```

**Response includes:**
- Each ride includes:
  - `id_rider` - Full user object (rider details)
  - `id_driver` - Full user object (driver details)
  - `todays_ride_events` - Array of ride events from the last 24 hours

#### Retrieve Single Ride
- **GET** `/api/rides/{id_ride}/`
- Returns a single ride with all related data

#### Rides with Duration
- **GET** `/api/rides/with_duration/`
- Returns rides with calculated trip duration
- **Query Parameters:**
  - `page` - Page number (default: 1)
  - `page_size` - Items per page (default: 10)
- **Response includes:**
  - `trip_duration_minutes` - Duration in minutes (if pickup and dropoff events exist)
  - `pickup_event_time` - ISO format timestamp of pickup event
  - `dropoff_event_time` - ISO format timestamp of dropoff event

### Ride Event Endpoints

- **GET** `/api/ride-events/` - List all ride events (admin only, paginated)
- **GET** `/api/ride-events/{id_ride_event}/` - Retrieve a specific ride event (admin only)
- **POST** `/api/ride-events/` - Create a new ride event (admin only)
- **PUT/PATCH** `/api/ride-events/{id_ride_event}/` - Update a ride event (admin only)
- **DELETE** `/api/ride-events/{id_ride_event}/` - Delete a ride event (admin only)

## Authentication & Authorization

### Requirements
- All API endpoints (except `/api/users/signin/` and `/api/users/signup/`) require authentication
- Only users with `role='admin'` can access the API endpoints

### How to Authenticate

**Option 1: Cookie-based (Recommended)**
After signing in or signing up, the authentication token is automatically stored in an `auth_token` cookie. Subsequent requests will automatically include this cookie.

**Option 2: Header-based**
Include the token in the Authorization header:
```
Authorization: Token <your-token-here>
```

### Creating an Admin User

1. Sign up with `role: "admin"`:
```bash
POST /api/users/signup/
{
  "email": "admin@example.com",
  "password": "admin123",
  "first_name": "Admin",
  "last_name": "User",
  "phone_number": "1234567890",
  "role": "admin"
}
```

2. Or use the seed_data command which creates admin users automatically

## Project Structure

```
todo_project/
├── manage.py
├── db.sqlite3
├── todo_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── user/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   ├── authentication.py
│   ├── permissions.py
│   └── token_utils.py
├── ride/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   ├── utils.py
│   └── management/commands/seed_data.py
└── ride_event/
    ├── models.py
    ├── views.py
    └── serializers.py
```

## Database

The project uses SQLite by default. The database file is located at:
```
todo_project/db.sqlite3
```

## Development

### Running Migrations

After making model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Admin

Access the Django admin panel at:
```
http://127.0.0.1:8000/admin/
```

## API Response Format

### Paginated Response
```json
{
  "count": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10,
  "next": "?page=2&page_size=10",
  "previous": null,
  "results": [...]
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error message here"
}
```

## Notes

- The API uses optimized database queries with `select_related()` and `prefetch_related()` to minimize database hits
- Ride list API uses 2 queries (or 3 with pagination count) to fetch rides with related users and events
- Distance sorting requires both `lat` and `lon` parameters along with `sort=distance` or `sort=-distance`
- All timestamps are in UTC timezone

## Troubleshooting

### Issue: "Module not found" errors
**Solution:** Make sure you're in the pipenv shell:
```bash
pipenv shell
```

### Issue: Database errors
**Solution:** Run migrations:
```bash
python manage.py migrate
```

### Issue: Authentication errors
**Solution:** 
1. Make sure you've signed in/signed up
2. Verify your user has `role='admin'`
3. Check that the authentication token is included in requests (cookie or header)

### Issue: Permission denied
**Solution:** Only users with `role='admin'` can access API endpoints. Create an admin user or use the seed_data command.
