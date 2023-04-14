from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated, AllowAny


class CustomPaymentView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "custom-payment.html"

    def get(self, request, *args, **kwargs):
        return Response({
            'content': "",
        })


class CreateCustomCheckoutSessionView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

    def post(self, request, *args, **kwargs):
        try:
            subscriber_no = request.data.get('subscriber_no', None)
            caregiver = request.data.get('caregiver', None)
            if subscriber_no == '' or subscriber_no == None:
                error_message = 'Please select subscriber_no'
                messages.error(request, error_message)
                return JsonResponse({
                    'error': error_message
                })
            subscriber_no = int(subscriber_no)
            amount = 369 * subscriber_no
            if caregiver == 'true':
                amount = amount + 100
            DOMAIN_URL = settings.HOST_DOMAIN
            amount = int(amount)*100

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {

                        'price_data': {
                            'currency': 'inr',
                            'unit_amount': amount,
                            'product_data': {
                                'name': 'Custom Subscriber Adding',
                            },

                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    'subscriber_no': subscriber_no,
                    'user_id': request.user.id,
                    'custom_subscriber_Adding': True
                },
                payment_intent_data={
                    "metadata": {
                        'subscriber_no': subscriber_no,
                        'user_id': request.user.id,
                        'custom_subscriber_Adding': True
                    },
                },
                mode='payment',
                success_url=DOMAIN_URL + 'custom_subscriber_success',
                cancel_url=DOMAIN_URL + 'payment?message=Failed',
            )
            return JsonResponse({
                'checkout_url': checkout_session.url
            })
        except Exception as e:
            print(e)
            error_message = 'Something Went Wrong !!!'
            messages.error(request, error_message)
            return JsonResponse({
                'error': error_message
            })


class CustomCheckoutSuccess(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "thankyou_new.html"

    def get(self, request, *args, **kwargs):
        info_message = 'Payment Processing Completed'
        messages.info(request, info_message)
        return Response({
            'content': "",
        })