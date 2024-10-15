# Django Project with JWT Authentication and Middleware for Token Handling

This project demonstrates how to configure a Django REST Framework application with JWT authentication, middleware for token handling, and API testing using Swagger UI.

## Table of Contents

- [Project Setup](#project-setup)
  - [Requirements](#requirements)
  - [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Development Server](#development-server)
  - [Using Docker](#using-docker)
- [Testing](#testing)
- [Measuring Test Coverage](#measuring-test-coverage)
- [Database Setup](#database-setup)
- [Creating a New User](#creating-a-new-user)
- [JWT Authentication](#jwt-authentication)
- [JWT Middleware](#jwt-middleware)
- [Swagger UI Setup](#swagger-ui-setup)

## Project Setup

### Requirements

- Python 3.x
- Django 3.x or higher
- Django REST Framework
- Django REST Framework Simple JWT
- drf-yasg for Swagger UI

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/arreolala/django_schedule.git
   cd django_schedule
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Server

1. **Run the Migrations**

   ```bash
   python manage.py migrate
   ```

2. **Start the Server**

   ```bash
   python manage.py runserver
   ```

3. **Access Swagger UI**

   Visit `http://127.0.0.1:8000/swagger/` to interact with the API documentation.

### Using Docker

1. **Build the Docker Image**

   Ensure a `Dockerfile` exists in your project directory. Build the image using:

   ```bash
   docker build -t django_schedule .
   ```

2. **Run the Container**

   ```bash
   docker run -p 8000:8000 django_schedule
   ```

   - For detached mode, use: `docker run -d -p 8000:8000 django_schedule`

3. **Using Docker Compose**

   If you have a `docker-compose.yml`, start all services with:

   ```bash
   docker-compose up
   ```

   - Use `-d` flag for detached mode: `docker-compose up -d`

4. **Stopping Services**

   - Single container: `docker stop <container_id>`
   - With Docker Compose: `docker-compose down`

## Testing

1. **Run Tests**

   Execute all test cases with:

   ```bash
   python manage.py test schedule_app
   ```

2. **Interpreting Test Results**

   - **PASS:** Functions as expected.
   - **FAIL:** Review errors and fix code.
   - **ERROR:** Investigate and resolve unhandled exceptions.

## Measuring Test Coverage

1. **Install Coverage.py**

   ```bash
   pip install coverage
   ```

2. **Run Coverage Analysis**

   ```bash
   coverage run manage.py test schedule_app
   ```

3. **Generate Coverage Report**

   View a report in the terminal:

   ```bash
   coverage report
   ```

4. **HTML Coverage Report**

   ```bash
   coverage html
   ```

   Open `htmlcov/index.html` in a browser for detailed coverage analysis.

## Database Setup

1. **Configure Database Settings**

   Examples for SQLite (default):

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / "db.sqlite3",
       }
   }
   ```

2. **Run Migrations**

   Set up schema:

   ```bash
   python manage.py migrate
   ```

## Creating a New User

1. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

2. **Follow Prompts**: Provide username, email, and password.

## JWT Authentication

1. **Install Simple JWT**

   Ensure `djangorestframework-simplejwt` is in your dependencies.

2. **Configure Authentication**

   In `settings.py`:

   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework_simplejwt.authentication.JWTAuthentication',
       ],
   }
   ```

3. **Add Token API Endpoints**

   In `urls.py`:

   ```python
   from django.urls import path
   from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

   urlpatterns = [
       path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
       path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   ]
   ```

## JWT Middleware

1. **Create Middleware**

   Example structure:

   ```plaintext
   schedule_app/
   ├── middleware/
   │   ├── __init__.py
   │   └── auth_prefix.py
   ```

2. **Middleware Logic**

   ```python
   from django.utils.deprecation import MiddlewareMixin

   class JWTAuthPrefixMiddleware(MiddlewareMixin):
       def __call__(self, request):
           auth_header = request.headers.get('Authorization', '')
           if auth_header and not auth_header.startswith('Bearer '):
               request.META['HTTP_AUTHORIZATION'] = f'Bearer {auth_header}'
           return self.get_response(request)
   ```

3. **Add Middleware to Settings**

   ```python
   MIDDLEWARE = [
       #... other middleware ...
       'schedule_app.middleware.auth_prefix.JWTAuthPrefixMiddleware',
   ]
   ```

## Swagger UI Setup

1. **Configure Schema View**

   In `urls.py`:

   ```python
   from django.urls import path
   from drf_yasg.views import get_schema_view
   from drf_yasg import openapi
   from rest_framework import permissions

   schema_view = get_schema_view(
       openapi.Info(
           title="Your API Title",
           default_version='v1',
           description="API Description",
           license=openapi.License(name="BSD License"),
       ),
       public=True,
       permission_classes=(permissions.AllowAny,),
   )

   urlpatterns += [
       path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
       path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   ]
   ```

2. **Swagger Settings**

   ```python
   SWAGGER_SETTINGS = {
       "USE_SESSION_AUTH": False,
       "SECURITY_DEFINITIONS": {
           "api_key": {"type": "apiKey", "name": "Authorization", "in": "header"},
       },
       "REFETCH_SCHEMA_WITH_AUTH": True,
   }
   ```
