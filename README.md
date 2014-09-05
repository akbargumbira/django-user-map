InaSAFE User Map
=================

A django application for InaSAFE user's map

This project replaces the simple flask based user map available here: 
https://github.com/kartoza/flask_user_map

Quick Start
============
1. Install all the requirements needed by User Map:
    ```
    pip install -r requirements.txt
    ```

2. Make sure you have all of these in INSTALLED_APPS in your project 
settings.py:
    ```
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.gis',
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

Apps Configurations
==================

Tile Layers
------------

You can configure the basemap of the form that uses LeafletWidget by adding 
'LEAFLET_CONFIG' in settings.py:

```
LEAFLET_CONFIG = {
    'TILES': [
        (
            'OpenStreetMap',
            'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
            ('© <a href="http://www.openstreetmap.org" '
             'target="_parent">OpenStreetMap</a> and contributors, under an '
             '<a href="http://www.openstreetmap.org/copyright" '
             'target="_parent">open license</a>')
        )]
}
```

Apps Configuration
------------------

You can also configure some variables by adding these items on your settings.py:

1. USER_MAP_PROJECT_NAME. This variable represents the project name of the 
   apps. If not specified, the default is 'InaSAFE'.
     
2. USER_MAP_BRAND_LOGO. This variable represents the file path to the brand 
   logo in navigation bar. If not specified, 
   the default is 'user_map/img/logo.png'
   
3. USER_MAP_FAVICON_FILE. This variable represents the file path to 
   the favicon on the tab. If not specified, 
   the default is 'user_map/img/user-icon.png'
   
4. USER_MAP_USER_ICONS. This variable is a dictionary that contains file 
   paths to the user icons that are used to represent markers at home page. 
   Right now it only supports 3 different kind of user: user, trainer, 
   developer. The default is:
   
   ```
   default_user_icons = dict(
        user='user_map/img/user-icon.png',
        trainer='user_map/img/trainer-icon.png',
        developer='user_map/img/developer-icon.png',
        shadow='user_map/img/shadow-icon.png'
   )
   ```
