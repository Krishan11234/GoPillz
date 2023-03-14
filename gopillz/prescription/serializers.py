from rest_framework import serializers, fields
from .models import *
from .helper import NUMBER_DAYS
from django.contrib.auth.hashers import make_password


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('subscriber_name',)


class MedicineSerializer(serializers.ModelSerializer):
    number_days = fields.MultipleChoiceField(choices=NUMBER_DAYS)

    class Meta:
        model = Medicine
        fields = ('medicine_name', 'medicine_type', 'schedule_time', 'level_of_engagement', 'datetime', 'number_days')


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ('doctor_name', 'doctor_phone_no', 'city', 'hospital_name', 'Ailment')


class CaregiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caregiver
        fields = ('caregiver_name', 'phone_no', 'email', 'relation',)


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def save_record(self, validated_data, user):
        info = {'status': '', 'message': ''}
        validated_data['is_staff'] = True
        validated_data['is_active'] = True
        validated_data['is_superuser'] = False
        validated_data['password'] = make_password(validated_data['password'])

        verified_email = EmailVerification.objects.filter(email=validated_data['email'])
        if verified_email:
            info['status'] = 'danger'
            info['message'] = 'Email address already present'
            return info

        EmailVerification.objects.create(user=user, email=validated_data['email'])
        user = User.objects.create(**validated_data)
        info['status'] = 'info'
        info['admin_details'] = validated_data
        info['message'] = 'Admin User Added Successfully'
        return info
