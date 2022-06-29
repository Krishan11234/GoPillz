from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Plan, PaymentMethod
from .serializers import PlanSerializer
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
import datetime


class PaymentView(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = None
    permission_classes = (AllowAny, )
    template_name = 'payment.html'
    plan_format = {
        'couple': 'Couple',
        'single': 'Single',
        'family_friends': 'Family&Friends',
    }

    def get(self, request):
        if not request.user.is_authenticated:
            error_message = 'Before Payment Please Verify Who you are'
            messages.info(request, error_message)
            return redirect('/signup')

        failed_message = request.query_params.get('message', '')
        if failed_message == 'Failed':
            error_message = 'Payment Request Failed or Cancelled'
            messages.info(request, error_message)
            get = request.GET.copy()
            del get['message']

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
            content['active_plan'] = request.query_params.get('val','yearly')
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
                        'unit_amount': int(amount),
                        'product_data': {
                            'name': plan_type,
                        },

                    },
                    'quantity': 1,
                },
            ],
            metadata={
                'payment_method': payment_method,
                'user_id': request.user.id,
                'plan_type': plan_type,
            },
            payment_intent_data={
                "metadata": {
                    'payment_method': payment_method,
                    'user_id': request.user.id,
                    'plan_type': plan_type,
                },
            },
            mode='payment',
            success_url=DOMAIN_URL+'success',
            cancel_url=DOMAIN_URL + 'payment?message=Failed',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class CheckoutSuccess(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "prescription.html"

    def get(self, request, *args, **kwargs):
        info_message = 'Payment Processing Completed'
        messages.info(request, info_message)
        return Response({
            'content': "",
        })


class CancelSuccess(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cancel.html"

    def get(self, request, *args, **kwargs):
        return Response({
            'content': "",
        })


class WebHooks(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.DJSTRIPE_WEBHOOK_SECRET)
        except Exception as e:
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            now = datetime.datetime.now()
            current_date = now.strftime("%Y/%m/%d")

            session = event['data']['object']
            metadata = session.get('metadata')
            plan = Plan.objects.get(price=session.get('amount_total', ''))
            payment_method = PaymentMethod.objects.get(method_name='Stripe')
            expires_at = session['expires_at']
            date = datetime.datetime.fromtimestamp(expires_at)
            str_expires_at = date.strftime("%Y/%m/%d")
            payment_data = {
                'payment_method': payment_method,
                'user_id': session.get('user_id', ''),
                'plan': plan,
                'expires_at': str_expires_at,
                'created_at': current_date
            }
            print(payment_data)

        return HttpResponse(status=200)