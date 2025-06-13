# Vacation Planner

A Django-based web application for planning and managing vacations.

## Features

- User registration and authentication
- View available vacations
- Like/unlike vacations (for regular users)
- Add, edit, and delete vacations (for admin users)
- Responsive design with Bootstrap
- REST API endpoints

## Technology Stack

- Backend: Django 5.0
- Database: PostgreSQL
- Frontend: HTML, CSS (Bootstrap 5), JavaScript
- Authentication: Django-allauth
- API: Django REST Framework

## Prerequisites

- Python 3.8 or higher
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vacation-planner
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=project_db
DB_USER=postgres
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432
```

5. Create the database:
```bash
createdb project_db
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create necessary directories:
```bash
mkdir static media
```

8. Populate the database with initial data:
```bash
python manage.py populate_db
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Visit http://127.0.0.1:8000/ in your browser

## Default Users

- Admin User:
  - Email: admin@example.com
  - Password: admin1234

- Regular User:
  - Email: user@example.com
  - Password: user1234

## Running Tests

```bash
python manage.py test
```

## API Endpoints

- `GET /api/vacations/` - List all vacations
- `POST /api/vacations/` - Create a new vacation (admin only)
- `GET /api/vacations/<id>/` - Get vacation details
- `PUT /api/vacations/<id>/` - Update vacation (admin only)
- `DELETE /api/vacations/<id>/` - Delete vacation (admin only)
- `POST /api/vacations/<id>/like/` - Like a vacation
- `DELETE /api/vacations/<id>/unlike/` - Unlike a vacation
- `GET /api/countries/` - List all countries
- `POST /api/countries/` - Create a new country (admin only)

## Project Structure

```
vacation-planner/
├── apps/
│   ├── accounts/      # User authentication and management
│   ├── core/          # Core functionality and models
│   └── vacations/     # Vacation management
├── config/            # Project settings
├── static/           # Static files
├── media/            # User-uploaded files
├── templates/        # HTML templates
└── manage.py         # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 