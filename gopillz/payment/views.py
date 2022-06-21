from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Plan
from .serializers import PlanSerializer
import stripe
from django.conf import settings
from django.http import JsonResponse


class PaymentView(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = None
    permission_classes = (IsAuthenticated,)
    template_name = 'payment.html'

    def get(self, request):
        plans = Plan.objects.all()
        plan_serializer = PlanSerializer(plans, many=True)
        content = {}
        try:
            content['plans'] = plan_serializer.data
            content['active_plan'] = 'yearly'
        except Exception as e:
            pass
        return Response({
            'content': content,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY_TEST
        })


class CreateCheckoutSessionView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

    def post(self, request, *args, **kwargs):
        DOMAIN_URL = 'http://127.0.0.1:8000/'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': 2000,
                        'product_data': {
                            'name': 'test'
                        }
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=DOMAIN_URL+'success',
            cancel_url=DOMAIN_URL + 'cancel',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class CheckoutSuccess(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    template_name = "success.html"

    def get(self, request, *args, **kwargs):
        DOMAIN_URL = ''


class CancelSuccess(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    template_name = "cancel.html"

    def get(self, request, *args, **kwargs):
        DOMAIN_URL = ''