from django.urls import path
from .views import PaymentView, CreateCheckoutSessionView, CheckoutSuccess, RenewSuccess, WebHooks
from .index_views import RenewSubscription, Proceed
from .CustomPayment import CustomPaymentView

urlpatterns = [
    path('payment/', PaymentView.as_view()),
    path('pay-now', RenewSubscription.as_view(), name='renew-subscription'),
    path('create-checkout-session', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success', CheckoutSuccess.as_view(), name='success'),
    path('renew-success', RenewSuccess.as_view(), name='renew-success'),
    path('stripe-webhooks', WebHooks.as_view(), name='stripe-webhooks'),
    path('proceed', Proceed.as_view(), name='proceed'),
    path('custom-payment/', CustomPaymentView.as_view()),
]