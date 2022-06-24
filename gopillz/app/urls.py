from django.urls import path
from .views import LandingPage, SignUp, Login, VerifyOtp, OtpVerification
from django.views.generic import RedirectView
from .index_views import Policy, UpdatePrescription, RenewSubscription

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('home/', LandingPage.as_view()),
    path('signup', SignUp.as_view()),
    path('login', Login.as_view(), name='login'),
    path('otp_verification', VerifyOtp.as_view(), name='otp_verification'),
    path('user_verification', OtpVerification.as_view(), name='otp-verify'),
    path('policy', Policy.as_view(), name='policy'),
    path('update-prescription', UpdatePrescription.as_view(), name='update-prescription'),
    path('renew-subscription', RenewSubscription.as_view(), name='renew-subscription')
]