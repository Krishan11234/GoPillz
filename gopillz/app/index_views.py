from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics
from django.contrib import messages
from django.shortcuts import redirect
from payment.models import Payment
import datetime


def check_expiry_date(exp_date):
    now = datetime.datetime.now()
    if exp_date.date() < now.date():
        return True
    if exp_date.date() == now.date():
        if exp_date.time() <= now.time():
            return True
    return False


class TermsCondition(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'terms_conditions.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class PrivacyPolicy(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'privacy_policy.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class RefundPolicy(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'refund_policy.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class Disclaimer(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'disclaimer.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class PrivacyNotice(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'privacy_notice.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class HowItWorks(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'how_it_works.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class Yearly(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'GoPillz-yearly.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class UpdatePrescription(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'prescription.html'

    def get(self, request):
        if not request.user.is_authenticated:
            error_message = 'Please sign up'
            messages.info(request, error_message)
            return redirect('/signup')
        payment_details = Payment.objects.filter(user=request.user)
        # if not payment_details:
        #     return redirect('/home')
        # data = payment_details.get()
        # exp_date_status = check_expiry_date(data.exp_date)
        # exp_date_status = False
        # if exp_date_status:
        #     messages.info(request, 'Subscription Expired Please Renew')
        #     return redirect('/home')
        content = {}
        return Response({'content': content})

