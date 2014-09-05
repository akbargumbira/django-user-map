InaSAFE User Map
=================

A django application for InaSAFE user's map

This project replaces the simple flask based user map available here: 
https://github.com/kartoza/flask_user_map

Quick Start
===========================
1. Install all the requirements needed by User Map:
```
pip install -r requirements.txt
```

2. Add 'user_map', 'leaflet', and 'bootstrapform' to your INSTALLED_APPS in 
your project settings.py so it looks like:
    ```
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        '......',
        'user_map',
        'leaflet',
        'bootstrapform'
    )
    ```

3. Include the user-map URLconf in your project urls.py like this:
    
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
4. Make sure to add template context processors needed by user-map: 

  ```
  TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'user_map.context_processors.user_map_settings',
  )
  ```

5. Make sure to add mail server configuration on your project's settings.py. 
If you are going to use SMTP server using your Gmail account, 
the configuration looks like this:

```
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'YOUR GMAIL ADDRESS'
    EMAIL_HOST_PASSWORD = 'YOUR GMAIL PASSWORD'
    DEFAULT_FROM_MAIL = 'MAIL ADDRESS AS THE DEFAULT SENDER'
```

6. Run ```python manage.py syncdb``` to create the user_map models. This will
   also prompt you to create a superuser. Create one so that you can log in to 
   django admin. Or you can do it later using ```python manage.py 
   createsuperuser``` 

7. Run ```python manage.py runserver``` to start the development server.

8. Visit http://127.0.0.1:8000/user-map/ to open the apps.

9. Visit your admin page (the default is http://127.0.0.1:8000/admin) to 
manage user as an admin. 

