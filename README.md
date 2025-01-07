# Join Backend

## A Django-based Backend project for a task management application. You can managing categories, tasks, subtasks and users. It provides REST-API endpoints for CRUD operations and user authentication.

This project is part of the Join-200 (Frontend).

## How to install this repository (Backend):

1. Clone this repository:
```
    git clone <GitHub repository link>
```

2. Create a virtual environment (in the project folder):
```
    python -m venv env
```

3. Install the dependencies:<br/>
activate the virtual environment
```
    pip install -r requirements.txt
```

4. Start the development server (on path: 127.0.0.1:8000):
```
    python manage.py runserver
```

5. Apply migrations:
```
    python manage.py makemigrations
    python manage.py migrate
```

6. Start Join-200 (Frontend):<br/>
clone the repository and run the liveserver on path 127.0.0.1:5500
