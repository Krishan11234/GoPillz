from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import SubscribeSerializer
from django.contrib import messages
from rest_framework.response import Response
from datetime import datetime
from django.http import JsonResponse
from .helper import get_email_verified_data
from django.shortcuts import redirect, render
from app.utils import Utils
from django.conf import settings
from payment.models import Payment

class Prescription(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = SubscribeSerializer
    template_name = "prescription.html"

    def post(self, request):
        request_data = self.prepare_request_data(request.data)
        subscriber_serializer = self.serializer_class(data=request_data)
        try:
            if subscriber_serializer.is_valid(raise_exception=True):
                saved_status = subscriber_serializer.save_record(validated_data=subscriber_serializer.validated_data, user=request.user)
                return JsonResponse(saved_status)

        except Exception as e:
            error_message = ' Failed Check Data and Try again'
            if 'username' in e.args[0]:
                error_message = str(e.args[0]['username'][0])

            return JsonResponse({
                'message': error_message,
                'status': 'danger'
            })

    def prepare_request_data(self, data):
        request_data = {}
        try:
            user_name = data.get('user_name', '')
            if len(user_name) > 0:
                request_data['username'] = user_name

            email = data.get('email', '')
            if len(email) > 0:
                request_data['email'] = email

            password = data.get('password', '')
            if len(password) > 0:
                request_data['password'] = password

            return request_data
        except Exception as e:
            return request_data

    def format_datetime(self, string_date):
        splitted_date = string_date.split(' ')
        date = splitted_date[0]
        am_pm_time = ' '.join(splitted_date[1:])
        hourly_time = self.timeConversion(am_pm_time).strip()
        date_time_str = date+' '+hourly_time
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y %H:%M')
        final_date_time_str = date_time_obj.strftime('%Y-%m-%d %H:%M')
        return final_date_time_str

    def timeConversion(self, s):
        if "PM" in s:
            s = s.replace("PM", " ")
            t = s.split(":")
            if t[0] != '12':
                t[0] = str(int(t[0]) + 12)
                s = (":").join(t)
            return s
        else:
            s = s.replace("AM", " ")
            t = s.split(":")
            if t[0] == '12':
                t[0] = '00'
                s = (":").join(t)
            return s


class AdminLoginView(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "prescription.html"
    verify_email_template = "verification_mail.html"
    admin_login_template = "admin_login.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            error_message = 'Please Sign Up Service not available'
            messages.info(request, error_message)
            return redirect('/signup')
        else:
            payment_data = Payment.objects.filter(user=request.user)
            if not payment_data:
                error_message = 'No Payment has been made please select plans'
                messages.info(request, error_message)
                return redirect('/payment')
        content = {}
        # info_message = 'Payment Processing Completed'
        varified_email = get_email_verified_data(request.user)
        if varified_email:
            if varified_email.verified:
                if varified_email.message_mail_sent:
                    info_message = 'Email Verified Successfully'
                    messages.info(request, info_message)
                    varified_email.message_mail_sent = False
                    varified_email.save()

                content['url'] = settings.USER_DASHBOARD
                content['user_name'] = varified_email.user.username
                return render(request, self.admin_login_template, content)
            else:
                content['email_address'] = varified_email.email
                return render(request, self.verify_email_template, content)

        # messages.info(request, info_message)
        return Response({
            'content': "",
        })


class UpdateEmail(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "verification_mail.html"
    admin_template_creation = "prescription.html"

    def get(self, request, *args, **kwargs):
        content = {}
        varified_email = get_email_verified_data(request.user)
        if varified_email:
            if varified_email.verified:
                return redirect('/signup')
        else:

            return render(request, self.admin_template_creation, content)
        content['email_address'] = varified_email.email
        info_message = ''
        messages.info(request, info_message)
        return render(request, self.template_name, content)
        # return Response({
        #     'content': content,
        # })


class SendMail(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "verify_email.html"
    admin_template_creation = "prescription.html"

    def post(self, request):
        if 'email' not in request.data:
            info_message = 'Incorrect request'
            messages.info(request, info_message)
            return Response({
                'content': {'message': 'fail'},
            })
        email_address = request.data['email']
        util_function = Utils(email_address)
        otp = util_function.generate_otp()
        context = "<p>Please Use OTP {} TO VERIFY ACCOUNT</p>".format(otp)
        util_function.send_email_using_sendgrid('Email Varification', context)
        # info_message = 'OTP Sent to the mail'
        # messages.info(request, info_message)
        long_string = util_function.generate_rand_string()
        data = get_email_verified_data(request.user)
        data.otp = otp
        data.rand_verification_string = long_string
        data.message_mail_sent = True
        data.save()

        return JsonResponse({
            'content': {'message': 'success',
                        'rand_string': long_string,
                        },
        })


class VerifyEmail(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "verify_email.html"
    admin_template_creation = "prescription.html"
    admin_login_template = "admin_login.html"

    def get(self, request, *args, **kwargs):
        content = {}
        varified_email = get_email_verified_data(request.user)
        if varified_email:
            if varified_email.verified:
                if varified_email.message_mail_sent:
                    info_message = 'Email Verified Successfully'
                    messages.error(request, info_message)
                    varified_email.message_mail_sent = False
                    varified_email.save()

                return render(request, self.admin_login_template, content)
        else:
            return render(request, self.admin_template_creation, content)

        content['email_address'] = varified_email.email

        if request.query_params:
            if 'sample_generator' in request.query_params:
                sample_str = request.query_params['sample_generator']
                if sample_str != varified_email.rand_verification_string:
                    info_message = 'Invalid Request'
                    messages.error(request, info_message)
                    return redirect('/home')

                if varified_email.message_mail_sent:
                    info_message = 'Mail Sent to the registered Email please Enter OTP Below'
                    messages.info(request, info_message)
                    varified_email.message_mail_sent = False
                    varified_email.save()

        return render(request, self.template_name, content)

    def post(self, request):
        otp = ''
        email = ''
        if 'otp' in request.data:
            otp = request.data['otp']

        if 'email' in request.data:
            email = request.data['email']

        varified_email = get_email_verified_data(request.user)
        if varified_email:
            if varified_email.otp == otp:
                varified_email.verified = True
                varified_email.message_mail_sent = True
                varified_email.save()
                return JsonResponse({
                    'status': 'success'
                })

        email_address = varified_email.email
        info_message = 'OTP Verification Failed'
        return JsonResponse({
            'email_address': email_address,
            'message': info_message,
            'status': 'danger'
        })