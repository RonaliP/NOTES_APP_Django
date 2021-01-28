from django.urls import path
from .views import RegisterView,VerifyEmailid,\
    LoginAPIView,ResetPassword,NewPassword,LogoutView,UserProfileView


#for swagger the below from here


urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('email-verify/',VerifyEmailid.as_view(),name="email-verify"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('new-password/', NewPassword.as_view(), name='new-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile')

]