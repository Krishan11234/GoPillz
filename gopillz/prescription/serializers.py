from rest_framework import serializers, fields
from .models import *
from .helper import NUMBER_DAYS


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
        model = Subscriber
        fields = ('subscriber_name', 'phone_number', 'address', 'city','country','pin_code')

    def save_record(self, validated_data, user):
        validated_data['added_by'] = user
        Subscriber.objects.create(**validated_data)
