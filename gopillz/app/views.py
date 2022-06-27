from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserProfileSerializer, UserVerification, ContactUsSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .utils import Utils
from django.conf import settings
from django.contrib import messages


"""
api view for the landing page
"""


class LandingPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        content = {}
        type = request.query_params.get('type', '')
        # if len(type) > 0:
        #     return Response(content, template_name='GoPillz-yearly.html')
        return Response({'content': content})


class OtpVerification(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    renderer_classes = [TemplateHTMLRenderer]
    success_template = 'verifynumber.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class SignUp(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    renderer_classes = [TemplateHTMLRenderer]
    util_instance = Utils()
    template_name = 'signup.html'
    success_template = 'verifynumber.html'

    def get(self, request):
        content = {}
        return render(request, self.template_name, content)

    # @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            data = self.create_user_data(request.data)
            serializer = self.get_serializer(data=data)
            # if serializer.is_valid(raise_exception=True):
            #     pass
            serializer.create(validated_data=data)
            context = {'phone_no': data['phone']}
            if self.send_otp_to_mobile(data):
                error_message = 'OTP Sent Please Verify'
                messages.success(request, error_message)
                return render(request, self.success_template, context)

            return self.default_error_response(request)
        except Exception as e:
            return self.default_error_response(request)

    def default_error_response(self, request):
        error_message = 'Cannot Send OTP please Try after Some Time'
        messages.error(request, error_message)
        response = Response()
        response['status'] = False
        return response

    def create_user_data(self, data):
        dict_data = {}
        phone_no = data.get('phone', '')
        if len(phone_no) > 0:
            unique_value = phone_no + '@gopillz.com'
            try:
                user = User.objects.get(username=unique_value)
                dict_data['user'] = user
            except Exception as e:
                user = None
            if user is None:
                dict_data['username'] = unique_value
                dict_data['email'] = unique_value
            dict_data['phone'] = phone_no
            otp = self.util_instance.generate_otp()
            dict_data['otp'] = otp
        return dict_data

    def send_otp_to_mobile(self, data):
        message = settings.SMS_MESSAGE.format(data['otp'])
        return self.util_instance.send_sms_using_twilio(message, data['phone'])


class Login(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'verifynumber.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class VerifyOtp(generics.GenericAPIView):
    serializer_class = UserVerification

    template_name = 'verifynumber.html'

    def get(self, request):
        content = {}
        return Response({'content': content})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(username=request.data['phone_no']+'@gopillz.com')
            if user:
                user_data = user[0]
                profile_data = user_data.profile
                if request.data['otp'] == str(profile_data.otp) and not profile_data.expired:
                    profile_data.expiry = True
                    profile_data.save()
                    user_auth = authenticate(username=user_data.username, password=settings.DEFAULT_USER_PASSWORD)
                    login(request, user_auth)
                    return redirect('/payment')
        error_message = 'OTP Verification Failed'
        messages.error(request, error_message)
        return redirect('/signup')


class ContactUs(generics.GenericAPIView):
    serializer_class = ContactUsSerializer

    def post(self, request):
        contact_us_serializer = self.serializer_class(data=request.data)
        try:
            response = Response()
            if contact_us_serializer.is_valid(raise_exception=True):
                contact_us_serializer.create(validated_data=contact_us_serializer.validated_data)
                error_message = 'Message Sent Successfully We will Update You shortly'
                messages.success(request, error_message)
                response['status'] = True
                return response

            error_message = 'Error in the Data Please Verify and Try again'
            messages.error(request, error_message)
            response['status'] = False
            return response
        except Exception as e:
            error_message = 'Error in the Data Please Verify and Try again'
            messages.error(request, error_message)
            response['status'] = False
            return response