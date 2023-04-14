from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import authenticate, login
from app.models import Profile
from django.contrib.auth.models import User


class CustomLogin(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        context = {'login_request': 'Failed'}
        try:
            user_name = request.data.get('user_name', '')
            user = User.objects.filter(username=user_name)
            if user:
                user_profile_data = Profile.objects.filter(user=user[0])
                if user_profile_data:
                    profile_data = user_profile_data[0]
                    user_auth = authenticate(username=profile_data.user_name, password=profile_data.password)
                    login(request, user_auth)
                    context['login_request'] = 'Success'

            return Response(context)
        except Exception as e:
            return Response(context)
