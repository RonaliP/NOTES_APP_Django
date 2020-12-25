from django.db import models

from django.contrib.auth.models import \
    (AbstractBaseUser,BaseUserManager,PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self,firstname,lastname,email,username,password=None):
        if username is None:
            raise TypeError('Users must have one username')
        if email is None:
            raise TypeError('Users must have emailid')

        user=self.model(firstname=firstname,lastname=lastname,username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,firstname,lastname, username, email, password=None):
        if password is None:
            raise TypeError('password cant be blank')



        user=self.create_user(firstname,lastname,username,email,password)
        user.is_superuser=True
        user.is_staff=True

        user.save()
        return user


class User(AbstractBaseUser,PermissionsMixin):
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    username=models.CharField(max_length=200,unique=True,db_index=True)
    email = models.CharField(max_length=200, unique=True, db_index=True)
    is_verified=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    objects=UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        return ''
