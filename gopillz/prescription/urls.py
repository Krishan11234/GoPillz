from django.urls import path
from .views import *


urlpatterns = [
    path('prescription', Prescription.as_view()),
    path('update-prescription', PrescriptionView.as_view())
]
