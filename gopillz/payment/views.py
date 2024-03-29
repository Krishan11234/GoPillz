from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Plan, PaymentMethod, Payment, SubscriberCount
from .serializers import PlanSerializer, PaymentSerializer
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from app.utils import Utils
import datetime
import json
from .helper import PLAN_CHOICES

plan_format = {
    'couple': 'Couple',
    'single': 'Single',
    'family_friends': 'Family&Friends',
}


default_subscriber_added = {
    'couple': 2,
    'single': 1,
    'family_friends': 4,
}


class PaymentView(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = None
    permission_classes = (AllowAny,)
    template_name = 'payment.html'

    def get(self, request):
        if not request.user.is_authenticated:
            error_message = 'Please sign up to purchase plan'
            messages.info(request, error_message)
            return redirect('/signup')
        try:
            subscription_data = Payment.objects.get(user_id=request.user.id)
            return redirect('/pay-now')
        except Exception as e:
            pass
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
                temp_plan_row['id'] = plan['id']
                temp_plan_row['plan_type'] = plan['plan_type']
                temp_plan_row['plan_name'] = plan_format[plan['plan_type']]
                temp_plan_row['duration'] = plan['duration']
                temp_plan_row['price'] = plan['price']
                content['plans'].append(temp_plan_row)
            if request.query_params.get('val', '') == 'yearly':
                content['active_plan'] = 'yearly'
            else:
                content['active_plan'] = 'monthly'
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
        try:
            payment_method = request.data.get('payment_method')
            plan_type = ''
            amount = ''
            plan_id = request.data.get('id', '')
            if plan_id == '':
                error_message = 'Please Select Plan'
                messages.error(request, error_message)
                return JsonResponse({
                    'error': error_message
                })

            plan = Plan.objects.filter(id=plan_id)
            if plan:
                plan_data = plan.get()
                plan_type = plan_format[plan_data.plan_type]
                amount = plan_data.price

            if plan_type == '' and amount == '':
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
            renew_subscription = request.data.get('renew-subscription')
            success_url_ = DOMAIN_URL + 'success',
            cancel_url_ = DOMAIN_URL + 'payment?message=Failed',
            amount = int(amount)*100
            if renew_subscription == True:
                success_url_ = DOMAIN_URL + 'renew-success'
                cancel_url_ = DOMAIN_URL + 'pay-now'
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'inr',
                                'unit_amount': amount,
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
                        'plan_id':plan_id
                    },
                    payment_intent_data={
                        "metadata": {
                            'payment_method': payment_method,
                            'user_id': request.user.id,
                            'plan_type': plan_type,
                            'plan_id': plan_id
                        },
                    },
                    mode='payment',
                    success_url=DOMAIN_URL + 'renew-success',
                    cancel_url=DOMAIN_URL + 'pay-now',
                )
                return JsonResponse({
                    'id': checkout_session.id
                })

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {

                        'price_data': {
                            'currency': 'inr',
                            'unit_amount': amount,
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
                    'plan_id': plan_id
                },
                payment_intent_data={
                    "metadata": {
                        'payment_method': payment_method,
                        'user_id': request.user.id,
                        'plan_type': plan_type,
                        'plan_id': plan_id
                    },
                },
                mode='payment',
                success_url=DOMAIN_URL + 'success',
                cancel_url=DOMAIN_URL + 'payment?message=Failed',
            )
            return JsonResponse({
                'id': checkout_session.id
            })
        except Exception as e:
            print(e)
            error_message = 'Something Went Wrong !!!'
            messages.error(request, error_message)
            return JsonResponse({
                'error': error_message
            })


class CheckoutSuccess(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "thankyou2.html"

    def get(self, request, *args, **kwargs):
        info_message = 'Payment Processing Completed'
        messages.info(request, info_message)
        return Response({
            'content': "",
        })


class RenewSuccess(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "thankyou.html"

    def get(self, request, *args, **kwargs):
        return Response({
            'content': "",
        })


class WebHooks(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def load_session_data(self, data):
        json_data = json.loads(data.decode('utf8'))
        print(json_data['data']['object']['status'])
        return json_data

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.DJSTRIPE_WEBHOOK_SECRET)
            print(event['type'])
        except Exception as e:
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            now = datetime.datetime.now()
            current_date = now.strftime("%Y-%m-%d %H:%M:%S")

            session = event['data']['object']
            metadata = session.get('metadata')
            if metadata.get('custom_subscriber_Adding', None):
                subscriber_no = metadata.get('subscriber_no')
                user_id = metadata.get('user_id')
                subscriber_count = SubscriberCount.objects.filter(user=user_id)
                if subscriber_count:
                    subscriber_count = subscriber_count[0]
                    subscriber_count.total_subscriber_count = subscriber_count.total_subscriber_count+int(subscriber_no)
                    subscriber_count.save()

                return HttpResponse(status=200)

            plan = Plan.objects.filter(id=metadata.get('plan_id', ''))
            if not plan:
                return HttpResponse(status=400)
            plan = plan.get()
            total_subscriber_count = default_subscriber_added[plan.plan_type]
            SubscriberCount.objects.create(user_id=metadata.get('user_id', ''), total_subscriber_count=total_subscriber_count)
            payment_method = PaymentMethod.objects.filter(method_name='Stripe')
            if not payment_method:
                return HttpResponse(status=400)
            expires_at = session['expires_at']
            date = datetime.datetime.fromtimestamp(expires_at)
            str_expires_at = date.strftime("%Y-%m-%d %H:%M:%S")

            payment_data = {
                'payment_method_id': payment_method[0].id,
                'user_id': metadata.get('user_id', ''),
                'plan_id': plan.id,
                'expired': False,
                'exp_date': str_expires_at,
                'created': current_date,
                'payment_status': session.get('status', 'Incomplete'),
            }

            payment_serializer = PaymentSerializer(data=payment_data)
            if payment_serializer.is_valid():
                payment_serializer.create(validated_data=payment_data)
            print('plan successfully assigned to the user')
            if 'customer_details' in session:
                customer_details = session['customer_details']
                if 'email' in customer_details:
                    email_id = customer_details['email']
                    util_obj = Utils(email_id)
                    context = '<p>Congratulations you have successfully activated your gopillz {} {} plan</p>'.format(plan.plan_type, plan.duration)
                    util_obj.send_email_using_sendgrid('Payment Success', context)

        return HttpResponse(status=200)
