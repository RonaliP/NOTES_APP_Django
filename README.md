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
 
 ##Create Models:
 
   -There are two models in authentication app:
      -User
      -Profile
   -There are two models in Notes app:
      -Notes
      -Labels
##Migration:
_In Terminal_
-migrate : python manage.py makemigrations

-makemigrations : python manage.py migrate
   
#SERIALIZERS

-Create serializers.py file inside the authentication app and create following serializer for every view in the views.py:

   -RegisterSerializer
   -EmailVerificationSerializer
   -LoginSerilaizer
   -ResetPasswordSerializer
   -NewPasswordSerializer
   -UserProfilrSerializer

-Create following serializer for notes app:

   -NotesSerializer
   -LabelsSerializer
   -ArchiveNotesSerializer
   -TrashSerializer
   -AddNotesInLabelsSerializer
   -AddLabelsToNoteSerializer

 -Create views for authentication:
 
 1.Registerview:
    -Create a view by extending CreateAPIView. The serializer_class tells which serializer to use and the permission_classes handles who can access the API.

   -Allow any user (authenticated or not) to hit this endpoint.

   -serializer = self.serializer_class(data=request.data) restore those native datatypes into a dictionary of validated data.

   -serializer.is_valid(raise_exception=True) checks if the data is as per serializer fields otherwise throws an exception.

   -serializer.save() to return an object instance, based on the validated data.

   -Generate jwt token using user details :

    payload = jwt_payload_handler(user)
    token = jwt.encode(payload,settings.SECRET_KEY)   
   -Create email verification link :

     absurl = 'http://'+current_site+relativeLink+'?token='+str(token)
   -Short this link by using pyshortners.

   -Send token on given email id:

   -Create a file in app named as Utils.py :

     from django.core.mail import EmailMessage
   -Using EmailMessage() we can send this verification link on email.

   -Other variables need to be set to send email: In settings.py:

     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
     EMAIL_USE_TLS = True
     EMAIL_HOST = 'smtp.gmail.com'
     EMAIL_PORT = 587
     EMAIL_HOST_USER = 'abc@gmail.com'
     EMAIL_HOST_PASSWORD = '***'
     
2. VerifyEmail view:

   -Get token from url and decode it to fetch user details.

   -Check token validations.If not then raise jwt errors.

   -Set the is_active and is_verified field as true :

       payload = jwt.decode(token,settings.SECRET_KEY)
       user = User.objects.get(id=payload['user_id'])
       if not user.is_verified:
         user.is_verified=True
         user.is_active=True
         user.save()
	 
3. LoginView:
   -Create a post method.

   -Set serializer class and pass request data to it for validations.

   -Check if user exists or not, if not then raise error.
   ```python
    def validate(self, attrs):
      email= attrs.get('email','')
      password = attrs.get('password','')
      try:
          user = User.objects.get(email =email, password=password)
          if not user:
              raise AuthenticationFailed("Invalid credentials given!!!")
          if not user.is_active:
              raise AuthenticationFailed("Account is deactivated!!!")
          if not user.is_verified:
              raise AuthenticationFailed("Email is not verified!!!")
      except serializers.ValidationError as identifier:
          return {'error':"Please provide email and password"}
      return {
          'email':user.email,
          'username':user.username,
          'password':user.password,
      }
    ```
4. ResetPassword View:
   -Take email from user validates it to generate jwt token.
   
   -Create link using token and send it to user email.
   
   -If email does not exist then raise validation error.
   
   -Use pyshortners to short this verification link.

5. NewPassword View:
   -Get token from url and decode it using jwt.decode().

   -fetch user details from it.

   -check if token is valid or not, if it is then set new validated password for user.

   -Otherwise raise jwt exceptions.
    
    ```python
     try:
      payload = jwt.decode(token,settings.SECRET_KEY)
      user = User.objects.get(id=payload['user_id'])
      user.password = user_data['password']
      user.save()    
      return Response({'email':'New password is created'},status=status.HTTP_200_OK)
  except jwt.ExpiredSignatureError as identifier:
      return Response({'error':'Link is Expired'}, status=status.HTTP_400_BAD_REQUEST)
  except jwt.exceptions.DecodeError as identifier:
      return Response({'error':'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)```
  
  
5. Logout View:
   -Set permsission as IsAuthenticated. So only authenticated and logged in user will be able to access it.
  
  -Call logout()
6. Profile view:
   -Use RetreiveUpdate from generics that will provide views to update user profile.

   -to get current user profiel rewrite the get_object method :

       def get_object(self):
         return self.request.user.profile
      
##View for notes app:

-Every view is a calss based and following attribues need to be set for each:

   -serializer_class : serilaizer class
   -queryset : Model object
   -permission_classes = (permissions.IsAuthenticated, IsOwner)
1. CraeteAndListNotes :
   -It will extend CreateAndListView from generics of rest frame work.
   -It provides following views :
      -Post : To create a new note.
      -Get : To list all created notes for a user.
   -1Pass request data to NotesSerializer for validation and serialized data with current user id.
   -Re write perform_create method to save data and get_queryset() to get records from database.
2. NoteDetails view:
   -It extends RetrieveUpdateDestroyView from generics.
   -It provides look-up field to get note by its id.
   -It provides views :
      -get : To retrieve note .
      -(put, patch) : To update note .
      -delete : To delete note.
3. CreateAndListLabels view :
   -It will extend CreateAndListView from generics of rest frame work.
   -It provides following views :
      -Post : To create a new label.
      -Get : To list all created labels for a user.
4. LabelDetails view:
   -It extends RetrieveUpdateDestroyView from generics.
   -It provides look-up field to get note by its id.
   -It provides views :
      -get : To retrieve label.
     -(put, patch) : To update label.
      -delete : To delete label.
5. ArchiveNote view:
   -It extends RetrieveUpdateDestroyView from generics.
   -It provides look-up field to get note by its id.
   -It provides views :
      -(put, patch) : To update archive field's value of note.
6. NoteToTrash view :
   -It extends RetrieveUpdateDestroyView from generics.
   -It provides look-up field to get note by its id.
   -It provides views :
      -(put, patch) : To update isDelete field's value of note.
7. ArchiveNotesList view :
   -It extends ListAPIView from generics.
   -It provides views :
      -get : To get all notes with archive field's value as true.
8. TrashList view :
   -It extends ListAPIView from generics.
   -It provides views :
      -get : To get all notes with isDelete field's value as true.
9. AddLabelsToNote view :
   -It extends RetrieveUpdateDestroyView from generics.

   -It provides look-up field to get note by its id.

   -It provides views :

      -(put, patch) : To update add label list to note.
10. ListNotesInLabel view :
   -Use same serializer class as AddLabelsToNote view.

   -Rewite the get_queryset() to filter queryset according to label id given in lookup field:
   -It provides views :

      -get : To get all notes list with smae label.
11. SearchNote view :
   -Get the search parameter and pass it to the get_queryset() :

      Request.GET.get('search')
   -Override the get_queryset() to match the search parameter with records data.

   -To match the search query parameter with model field data, use icontains lookup. It matches the data case insensetive :

      fieldname__icontains
12. AddCollaborator view :
   -Create a field in notes model to add collaborator.
   -Give pemission to added user in colloborator field to access note .
   -To give permissions overrid the permission methods.
 
##Create route

-For every view we have to create route in urls.py in its correspnding app.

-To access these APIs the corrosponding path has to be provided on localhost.

     urlpatterns = [
      path('register/',RegisterView.as_view() , name='register'),
      path('login/',LoginAPIView.as_view() , name='login'),
      path('logout/', LogoutView.as_view(), name='logout'),
      path('verify-email/',VerifyEmail.as_view() , name='verify-email'),
      path('reset-password/',ResetPassword.as_view() , name='reset-password'),
      path('new-pass/', NewPassword.as_view(), name='new-pass'),
      path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
    
    
##Redis Installation :
About redis : Redis is an in-memory data structure store that can be used as a caching engine. Since it keeps data in RAM, Redis can deliver it very quickly. Redis is not the only product that we can use for caching.
Use this link to download redis for windows: https://github.com/MicrosoftArchive/redis/releases
Download and run .msi file for installation.

Redis cache implementation :
Set custom cache backend in settings :

  CACHES = {
      "default": {
          "BACKEND": "django_redis.cache.RedisCache", 
          "LOCATION": "redis://127.0.0.1:6379/1",
          "OPTIONS": {
              "CLIENT_CLASS": "django_redis.client.DefaultClient",
              "TIMEOUT": 3600
          },
          "KEY_PREFIX": "keep"
      }
  }
##Accessing the cache:

         import : from django.core.cache import cache
         cache.set(key, value, timeout=DEFAULT_TIMEOUT, version=None)
         cache.get(key, default=None, version=None)
-For each API call check if data is present in cache or not by using cache.get(key).

-If it is there then retrieve data from to cache only otherwise perform query on database and set that data to cache by using cache.set(key, data). So that next time that data can be retrieved from cache.

##RabbitMQ Installation:
   -First we need to download and install erlang from the given link for windows: https://erlang.org/download/otp_versions_tree.html
   -Then we need to download and install rabbitMQ server for windows : https://www.rabbitmq.com/install-windows.html

   -then go to start menu and search for rabbitmq command prompt

   -type command "rabbitmq-plugins enable rabbitmq_management"

   -All set to go now go to http://localhost:15672

   -Use following credentials for authentication:

     username: guest
     passowrd: guest
     
##Celery:
-Add the CELERY_BROKER_URL configuration to the settings.py file :

      CELERY_BROKER_URL = 'amqp://localhost'
-In project root folder create a new file named celery.py and add the following code in that :

      import os
      from celery import Celery
      os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
      app = Celery('project_name')
      app.config_from_object('django.conf:settings', namespace='CELERY')
      app.autodiscover_tasks()
-Now edit the init.py file in the project root:

      from .celery import app as celery_app
      __all__ = ['celery_app']
-Create a file named tasks.py inside a Django app and put all our Celery tasks into this file. Basic structure is here :

      from celery import shared_task

      @shared_task
      def name_of_your_function(optional_param):
          pass  # do something heavy
-Starting The Worker Process : Open a new terminal tab, and run the following command:

      celery -A mysite worker -l info
