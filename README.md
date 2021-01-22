# NOTES_APP_Django
### Description :

	This is Notes app which is built using Django which tries to clone the behaviour of Google's Keep Notes app.
	in which rest APIs are created for authentication of users and all Notes operations.

>_Lets start with the project i created first(I used pycharm as IDE)_

**I created TODO_LIST project first by command(django-admin startproject TODO_LIST)**

(You can follow django official documentation for all the steps)

- I created two django apps inside TODO_LIST:

   - authentication
   - Notes
 

- authentication app provides APIs for following features:

   - Registration
   - email verification by sending token to user's email.
   - Login and logout
   - Reset password
   - UserProfile
-For authentication JWT token is used.

-For user profile creation signal is used.

-Notes app provides APIs for following features :
   
      -Create and list notes
      -Create and list labels
      -Archive note
      -Trash note
      -Update note
      -Update label
      -Delete note
      -Delete label
      -Retrieve Note
      -Retrieve label
      -List all archived notes
      -List all trashed notes
      -Add labels to a note
   
 #1. (FIRST_STEP)Creation of Django-Project :
    - Create a virtual environment first inside which we will install all the requirements
    
    _ For windows : python -m venv enviromentname _

   -Activate the virtual environment :enviromentname/Script/activate
   
      -Install Requirements of this project:
      -pip install django
      -pip install djangorestframework
      -pip install django-rest-framework jwt
      -pip install pyshortners
      -pip install django-redis
      -pip install celery
      -pip install django-celery-results
      -pip install django-celery-beat
      -pip install psycopg2

# Start the project now:
   -create our project using a command-line utility provided by django.

      -django-admin startproject TODO_LIST
      
 _Now to check whether all the installments are done properly and to check if the server is running properly_
 
    -Try this command to start server :python manage.py runserver
      
 - Hit http://127.0.0.1:8000/ 
 
 #Start with creating apps:
 
    -python manage.py startapp app name(in my case its authentication)
    
 - Configure the app

   - Create file in urls.py inside app.

   - Inside project root directory add the path of this created urls.py in app :

     - path('authentication/',include('authentication.urls'))
   - Inside app in the urls.py file add route for view created in app.

-Same steps will be repeated for Notes app.

# Register apps inside project's app which is TODO_LIST:
   - inside settings.py
   
       INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'rest_framework',
      'authentication.apps.AuthenticationConfig',
      'notes',
  ]

# Register models in admins.py of authentication app:
   
  from django.contrib import admin
  from authentication.models import User, UserProfile
  admin.site.register(User)
  admin.site.register(UserProfile)
 _same for Notes app_
 
# Database connection with project:

   - settings.py file:
   
   _i used postgres_
   
       DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'database name',
         'USER': 'postgres',
         'PASSWORD': 'password',
         'PORT': '5432',
     }
 }
   


 


