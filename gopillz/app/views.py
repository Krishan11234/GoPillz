from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserProfileSerializer, UserVerification
from rest_framework import generics, permissions
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
        return Response({'content': content})


class SignUp(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    renderer_classes = [TemplateHTMLRenderer]
    util_instance = Utils()
    template_name = 'signup.html'
    success_template = 'verifynumber.html'

    def get(self, request):
        content = {}
        return Response({'content': content})

    # @method_decorator(csrf_exempt)
    def post(self, request):
        data = self.create_user_data(request.data)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.is_valid(raise_exception=True)
        serializer.create(validated_data=data)
        context = {'phone_no': data['phone']}
        self.send_otp_to_mobile(data)
        return render(request, self.success_template, context)

    def create_user_data(self, data):
        dict_data = {}
        phone_no = data.get('phone', '')
        if len(phone_no) > 0:
            unique_value = phone_no + '@gopillz.com'
            user = User.objects.get(username=unique_value)
            if user is None:
                dict_data['username'] = unique_value
                dict_data['email'] = unique_value
            dict_data['user'] = user
            dict_data['phone'] = phone_no
            otp = self.util_instance.generate_otp()
            dict_data['otp'] = otp
        return dict_data

    def send_otp_to_mobile(self, data):
        message = settings.SMS_MESSAGE.format(data['otp'])
        self.util_instance.send_sms_using_twilio(message, data['phone'])


class Login(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'verifynumber.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class VerifyOtp(generics.GenericAPIView):
    serializer_class = UserVerification

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