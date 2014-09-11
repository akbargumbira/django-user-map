Django User Map
=================

A django application for making community user's map. Users can 
add themselves on the map by providing some information:
1. Name
2. E-mail - will be used for authentication
3. Password - will be used for authentication
4. Website
5. Role - The choices can be configured through setting.
6. Location on the map

Live site: http://users.inasafe.org

Installation
============
1. Install django-user-map with pip:
   ```
    pip install django-user-map
   ```

2. Make sure you have all of these items in INSTALLED_APPS of your django 
   project settings.py:
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

3. Include user-map URLconf in your project urls.py e.g:
   ```
    url(r'^user-map/', include('user_map.urls')),
   ```

3. Add authentication user model and authentication backend in your django 
   project settings.py:
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

5. Make sure to add mail server configuration on your project's settings.py 
   so that this apps can send e-mail for some routines e.g sending confirmation 
   e-mail after registration. If you are going to use SMTP server using your 
   Gmail account, the configuration looks like this:
    ```
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'YOUR GMAIL ADDRESS'
    EMAIL_HOST_PASSWORD = 'YOUR GMAIL PASSWORD'
    DEFAULT_FROM_MAIL = 'MAIL ADDRESS AS THE DEFAULT SENDER'
    ```

6. Run ```python manage.py migrate``` to create the user_map models. 

7. Create a superuser so that you can log in to django admin to administer 
user:
    ```python manage.py  createsuperuser``` 

7. Run ```python manage.py runserver``` to start the development server.

8. Visit http://127.0.0.1:8000/user-map/ to open the apps.

9. Visit your admin page (the default is http://127.0.0.1:8000/admin) to 
manage user as an admin. 


Apps Configurations
==================

Tile Layer
------------

You can configure the basemap of the form that uses LeafletWidget and the  
basemap of the homepage by adding 'LEAFLET_CONFIG' in settings.py e.g:
```
LEAFLET_CONFIG = {
    'TILES': [
        (
            'OpenStreetMap', # The title
            'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', # The tile URL
            ('© <a href="http://www.openstreetmap.org" '
             'target="_parent">OpenStreetMap</a> and contributors, under an '
             '<a href="http://www.openstreetmap.org/copyright" '
             'target="_parent">open license</a>') # The attribution
        )]
}
```

Configurable variables
----------------------

You can also configure some variables by adding these items on your 
django settings.py:

1. USER_MAP_PROJECT_NAME (string). This variable represents the project name of 
   the apps. If this is not specified, 'InaSAFE' will be used.
     
2. USER_MAP_BRAND_LOGO (string). This variable represents the file path to 
   the brand logo in navigation bar. If not specified, 
   'user_map/img/logo.png' will be used.
   
3. USER_MAP_FAVICON_FILE (string). This variable represents the file path to 
   the favicon on the browser's tab. If not specified,  
   the default is 'user_map/img/user-icon.png'
   
4. USER_MAP_USER_ROLES (list of dictionary). Using this variable, 
   you can specify the user's role and the icon path for the role. If not  
   specified, this variable will take this as the default:
   ```
   default_user_roles = [
      dict(
        name='User',
        icon='user_map/img/user-icon.png',
        shadow_icon='user_map/img/shadow-icon.png'),
      dict(
        name='Trainer',
        icon='user_map/img/trainer-icon.png',
        shadow_icon='user_map/img/shadow-icon.png'),
      dict(
        name='Developer',
        icon='user_map/img/developer-icon.png',
        shadow_icon='user_map/img/shadow-icon.png')]
   ```
   While you can add as many roles as you want, note that we only create 
   three  css classes for the marker clusterer (it makes clusters of users 
   based on the role). If you want to have more than three roles, 
   you need to add these two classes with this pattern:
   ```
   .marker-cluster-role4 {
        background-color: rgba(253, 156, 115, 0.6);
   }
   .marker-cluster-role4 div {
        background-color: rgba(241, 128, 23, 0.6);
   }
   ```
