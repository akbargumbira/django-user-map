InaSAFE User Map
=================

A django application for InaSAFE user's map

This project replaces the simple flask based user map available here: 
https://github.com/kartoza/flask_user_map

Quick Start for Development
===========================
1. Add 'user_map' to your INSTALLED_APPS in your project settings.py like this:
    ```
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        '......',
        'user_map'
    )
    ```

2. Include the polls URLconf in your project urls.py like this::
    
    ```
    url(r'^user-map/', include('user_map.urls')),
    ```

3. Add authentication user model and authentication backend in your project 
  settings.py like this:
  
  ```
    AUTH_USER_MODEL = 'user_map.User'
    AUTHENTICATION_BACKENDS = [
        'user_map.auth_backend.UserMapAuthBackend',
        'django.contrib.auth.backends.ModelBackend']
  ```

4. Run ```python manage.py syncdb``` to create the user_map models. This will
   also prompt you to create superuser. Create one so that you can log in to 
   django admin. 

5. Run ```python manage.py runserver``` to start the development server.

6. Visit http://127.0.0.1:8000/user-map/ to participate in the map.

