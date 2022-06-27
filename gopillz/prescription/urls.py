from django.urls import path
from .views import *


urlpatterns = [
    path('prescription', Prescription.as_view()),
]
