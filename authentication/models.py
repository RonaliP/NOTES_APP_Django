from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import(AbstractBaseUser,BaseUserManager,PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self,firstname,lastname,email,username,password=None):
        if username is None:
            raise TypeError('User should have a username')

        if email is None:
            raise TypeError('User should have a Email')
        user=self.model(firstname=firstname,
                        lastname=lastname,
                        username=username,
                        email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,firstname,lastname,email,username,password=None):
        if password is None:
            raise TypeError('Password can not be none')

        user = self.create_user(firstname,lastname,username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser,PermissionsMixin):
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    username=models.CharField(max_length=200,unique=True, db_index=True)
    email = models.CharField(max_length=200, unique=True, db_index=True)
    is_verified=models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    objects=UserManager()
    def get_email(self):
        return self.email


    def __str__(self):
        return self.email


class Profile(models.Model):

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    DOB = models.DateField(max_length=8,null=True)
    BIO=models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pic')

    def get_image(self):
        return self.image

    def __str__(self):
        return str(self.user)





