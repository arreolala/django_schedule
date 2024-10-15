# Django Project with JWT Authentication and Middleware for Token Handling

This project demonstrates how to configure a Django REST Framework application with JWT authentication, middleware for token handling, and API testing using Swagger UI.

## Table of Contents

- [Project Setup](#project-setup)
  - [Requirements](#requirements)
  - [Installation](#installation)
- [Database Setup](#database-setup)
- [Creating a New User](#creating-a-new-user)
- [JWT Authentication](#jwt-authentication)
- [JWT Middleware](#jwt-middleware)
- [Swagger UI Setup](#swagger-ui-setup)
- [Running the Application](#running-the-application)
- [Testing the API](#testing-the-api)
- [Running Tests](#running-tests)

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
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
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

## Database Setup

1. **Configure Database Settings**

    Update your `settings.py` with your database configuration. For example, to use SQLite (default):

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }
    ```

2. **Run Migrations**

    Set up the database schema by running:

    ```bash
    python manage.py migrate
    ```

## Creating a New User

To test the authentication, you’ll need to create a user.

1. **Create a Superuser**

    Generate a superuser account for accessing the Django admin and performing tests:

    ```bash
    python manage.py createsuperuser
    ```

2. **Fill in the prompts** with your desired username, email, and password.

## JWT Authentication

1. **Install Simple JWT**

    Ensure that `djangorestframework-simplejwt` is in your list of dependencies and installed.

2. **Configure Authentication Classes**

    Update your Django settings to use JWT authentication:

    ```python
    # settings.py
    
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ],
    }
    ```

3. **Add Token Endpoints**

    Define the token obtain and refresh endpoints in your `urls.py`:

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

    Place the middleware at the project level if it affects multiple apps:

    ```plaintext
    schedule_app/
    ├── middleware/
    │   ├── __init__.py
    │   └── auth_prefix.py
    ```

2. **Define Middleware Logic**

    Implement middleware logic to handle the JWT header:

    ```python
    # auth_prefix.py
    
    from django.utils.deprecation import MiddlewareMixin
    
    class JWTAuthPrefixMiddleware(MiddlewareMixin):
        def __call__(self, request):
            auth_header = request.headers.get('Authorization', '')
            if auth_header and not auth_header.startswith('Bearer '):
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {auth_header}'
            return self.get_response(request)
    ```

3. **Add Middleware to Settings**

    Register the middleware in `settings.py`:

    ```python
    MIDDLEWARE = [
        #... other middleware ...
        'schedule_app.middleware.auth_prefix.JWTAuthPrefixMiddleware',
    ]
    ```

## Swagger UI Setup

1. **Schema View Configuration**

    Set up `drf-yasg` to serve your API documentation:

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
            contact=openapi.Contact(email="contact@example.com"),
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

    Add `SWAGGER_SETTINGS` in your `settings.py`:

    ```python
    SWAGGER_SETTINGS = {
        "USE_SESSION_AUTH": False,
        "SECURITY_DEFINITIONS": {
            "api_key": {"type": "apiKey", "name": "Authorization", "in": "header"},
        },
        "REFETCH_SCHEMA_WITH_AUTH": True,
    }
    ```

## Running the Application

1. **Start the Django Server**

    ```bash
    python manage.py runserver
    ```

2. **Access Swagger UI**

    Visit `http://127.0.0.1:8000/swagger/` to access and interact with the API documentation.

## Testing the API

1. **Obtain JWT Token**

    - Access the `/api/token/` endpoint via Swagger or a tool like Postman to obtain a JWT by providing your username and password.

2. **Authorize with JWT in Swagger**

    - Click "Authorize" in the Swagger UI and enter your token in the following format:
      ```
      Bearer <your_jwt_token>
      ```

    The middleware will ensure that the "Bearer " prefix is automatically handled if missing when using JWTs.

## Running Tests

To ensure your Django application is functioning as expected, you can run unit tests specifically designed to test features and functionalities within your `schedule_app`. Django's built-in test framework makes it easy to validate your code.

1. **Create Test Cases**

   Ensure you have written appropriate test cases in your `schedule_app`. Typically, test cases are placed in a `tests.py` file within the app directory or in a `tests` package with multiple files if the tests are extensive.

   Example of a basic test case in `schedule_app/tests.py`:

   ```python
   from django.test import TestCase
   from .models import DaySchedule
   from django.urls import reverse
   
   class DayScheduleTests(TestCase):
   
       def setUp(self):
           # Set up initial test data
           DaySchedule.objects.create(name="Test Schedule")
   
       def test_schedule_creation(self):
           # Test that a schedule can be created correctly
           schedule = DaySchedule.objects.get(name="Test Schedule")
           self.assertEqual(schedule.name, "Test Schedule")
   
       def test_schedule_list_view(self):
           # Test the list view for schedules
           response = self.client.get(reverse('day-schedule-list'))
           self.assertEqual(response.status_code, 200)
           self.assertContains(response, "Test Schedule")
   ```

2. **Run the Tests**

   Use Django's test command to run tests in your `schedule_app`:

   ```bash
   python manage.py test schedule_app
   ```

3. **Interpreting Test Results**

   - **PASS:** Tests have completed without errors, indicating expected functionality.
   - **FAIL:** A test's assertions were not met. Review which test failed and diagnose the issue.
   - **ERROR:** An unhandled exception occurred during a test. Check the stack trace for details and address the problem.
