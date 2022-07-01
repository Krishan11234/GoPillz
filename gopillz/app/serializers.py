from rest_framework import serializers, fields
from django.contrib.auth.models import User
from .models import Profile, ContactUs
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    A student serializer to return the student details
    """
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('user', 'otp',)

    def validate(self, attrs):
        phone_no = attrs.get('phone', '')
        pass

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = {}
        if 'user' in validated_data:
            user = validated_data.pop('user')
        else:
            user_data['email'] = validated_data.pop('email')
            user_data['username'] = validated_data.pop('username')
        password = settings.DEFAULT_USER_PASSWORD

        if user_data:
            user = UserSerializer.create(UserSerializer(), validated_data=user_data)
            user.set_password(password)
            user.save()
        try:
            user_profile = Profile.objects.get(user_id=user.id)
        except Exception as e:
            user_profile = None

        if user_profile is None:
            user_profile, created = Profile.objects.update_or_create(user=user, otp=validated_data['otp'], expired=False)
        else:
            user_profile.otp = validated_data['otp']
            user_profile.expired = False
            user_profile.save()

        return user_profile


class UserVerification(serializers.ModelSerializer):
    otp = serializers.IntegerField()
    phone_no = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('otp', 'phone_no')


class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        fields = ('email', 'first_name', 'last_name', 'phone_no', 'message')

    def create(self, validated_data):
        return ContactUs.objects.create(**validated_data)

