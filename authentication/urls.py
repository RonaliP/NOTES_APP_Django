from django.urls import path
from .views import RegisterView,VerifyEmailid,\
    LoginAPIView,ResetPassword,NewPassword,LogoutView


#for swagger the below from here


urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('email-verify/',VerifyEmailid.as_view(),name="email-verify"),
    path('Login/', LoginAPIView.as_view(), name="login"),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('new-pass/', NewPassword.as_view(), name='new-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]