from django.urls import path
from .views import LandingPage, SignUp, Login, VerifyOtp, OtpVerification, ContactUs, Logout, RegisteredUser
from django.views.generic import RedirectView
from .index_views import *

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('home/', LandingPage.as_view()),
    path('home_yearly/', Yearly.as_view()),
    path('signup', SignUp.as_view()),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('registered_user', RegisteredUser.as_view(), name='login'),
    path('otp_verification', VerifyOtp.as_view(), name='otp_verification'),
    path('user_verification', OtpVerification.as_view(), name='otp-verify'),
    path('terms_conditions', TermsCondition.as_view(), name='terms_conditions'),
    path('privacy_policy', PrivacyPolicy.as_view(), name='privacy_policy'),
    path('privacy_notice', PrivacyNotice.as_view(), name='privacy_notice'),
    path('disclaimer', Disclaimer.as_view(), name='disclaimer'),
    path('refund_policy', RefundPolicy.as_view(), name='refund_policy'),
    path('update-prescription', UpdatePrescription.as_view(), name='update-prescription'),
    path('contact_us', ContactUs.as_view(),name='contact-us'),
    path('how_it_works', HowItWorks.as_view(), name='how_it_works')
]