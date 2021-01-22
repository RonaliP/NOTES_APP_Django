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
6. UserProfile view:
   -Use RetreiveUpdate from generics that will provide views to update user profile.

   -to get current user profiel rewrite the get_object method :

       def get_object(self):
         return self.request.user.profile
      
