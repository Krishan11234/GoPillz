from django.urls import path
from .views import PaymentView, CreateCheckoutSessionView, CheckoutSuccess, CancelSuccess, WebHooks

urlpatterns = [
    path('payment/', PaymentView.as_view()),
    path('create-checkout-session', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success', CheckoutSuccess.as_view(), name='success'),
    path('cancel', CancelSuccess.as_view(), name='cancel'),
    path('stripe-webhooks', WebHooks.as_view(), name='stripe-webhooks')
]