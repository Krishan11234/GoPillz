from django.urls import path
from .views import PaymentView, CreateCheckoutSessionView, CheckoutSuccess, CancelSuccess

urlpatterns = [
    path('payment/', PaymentView.as_view()),
    path('create-checkout-session', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success', CheckoutSuccess.as_view(), name='success'),
    path('cancel', CancelSuccess.as_view(), name='cancel')
]