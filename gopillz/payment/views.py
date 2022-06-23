from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Plan
from .serializers import PlanSerializer
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages


class PaymentView(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = None
    permission_classes = (IsAuthenticated,)
    template_name = 'payment.html'
    plan_format = {
        'couple': 'Couple',
        'single': 'Single',
        'family_friends': 'Family&Friends',
    }

    def get(self, request):
        plans = Plan.objects.all()
        plan_serializer = PlanSerializer(plans, many=True)
        content = {'plans': []}
        try:
            for plan in plan_serializer.data:
                temp_plan_row = {}
                temp_plan_row['plan_type'] = plan['plan_type']
                temp_plan_row['plan_name'] = self.plan_format[plan['plan_type']]
                temp_plan_row['duration'] = plan['duration']
                temp_plan_row['price'] = plan['price']
                content['plans'].append(temp_plan_row)
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
        payment_method = request.data.get('payment_method')
        plan_type = request.data.get('plan_type')
        amount = request.data.get('amount')

        if plan_type=='' and amount =='':
            error_message = 'Select Plan Type'
            messages.error(request, error_message)
            return JsonResponse({
                'error': error_message
            })
        if payment_method is None:
            error_message = 'Select Atleast One payment Method'
            messages.error(request, error_message)
            return JsonResponse({
                'error': error_message
            })
        if payment_method not in ['stripe']:
            error_message = 'Invalid Payment Method please select Stripe.Others were in processing'
            messages.error(request, error_message)
            return JsonResponse({
                'error': error_message
            })
        DOMAIN_URL = settings.HOST_DOMAIN
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': amount,
                        'product_data': {
                            'name': plan_type
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
    template_name = "success.html"

    def get(self, request, *args, **kwargs):
        DOMAIN_URL = ''
        return Response({
            'content': "",
        })


class CancelSuccess(generics.GenericAPIView):
    template_name = "cancel.html"

    def get(self, request, *args, **kwargs):
        DOMAIN_URL = ''
        return Response({
            'content': "",
        })