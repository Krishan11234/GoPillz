from django.urls import path
from .views import *
from .CustomLogin import CustomLogin

urlpatterns = [
    path('verify_email', UpdateEmail.as_view()),
    path('prescription', Prescription.as_view()),
    path('login-admin', AdminLoginView.as_view()),
    path('send_mail', SendMail.as_view()),
    path('email-verification', VerifyEmail.as_view()),
    path('custom-login', CustomLogin.as_view())
]
