from django.urls import path
from .views import RegisterView,VerifyEmailid


#for swagger the below from here


urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('email-verify/',VerifyEmailid.as_view(),name="email-verify"),
]