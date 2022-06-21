from django.urls import path
from .views import LandingPage, SignUp, Login, VerifyOtp
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('home/', LandingPage.as_view()),
    path('signup', SignUp.as_view()),
    path('login', Login.as_view(), name='login'),
    path('otp_verification', VerifyOtp.as_view(), name='otp_verification')
]