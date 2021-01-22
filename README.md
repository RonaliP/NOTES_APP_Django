# NOTES_APP_Django
### Description :

	This is Notes app which is built using Django which tries to clone the behaviour of Google's Keep Notes app.
	in which rest APIs are created for authentication of users and all Notes operations.

>_Lets start with the project i created first_

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
For authentication JWT token is used.

For user profile creation signal is used.

notes app provides APIs for following features :


