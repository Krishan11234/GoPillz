from rest_framework import serializers
from .models import *


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('subscriber_name',)


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ('medicine_name', 'medicine_type', 'number_days', 'schedule_time', 'level_of_engagement')


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('doctor_name', 'doctor_phone_no', 'city', 'hospital_name', 'Ailment')


class CaregiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caregiver
        fields = ('caregiver_name', 'phone_no', 'email', 'relation',)


class PrescriptionSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(many=True, required=False)
    doctor = DoctorSerializer(many=True, required=False)
    caregiver = CaregiverSerializer(many=True, required=False)
    subscriber = SubscriberSerializer(many=True, required=False)

    class Meta:
        model = Prescription
        fields = ('medicine', 'doctor', 'caregiver', 'subscriber')

    def create(self, validated_data):
        medicine_data = None
        caregiver_data = None
        doctor_data = None
        if 'medicine' in validated_data['validated_data']:
            medicine_data = validated_data['validated_data'].pop('medicine')
            medicine_data = Medicine.objects.create(**medicine_data[0])

        if 'caregiver' in validated_data['validated_data']:
            caregiver_data = validated_data['validated_data'].pop('caregiver')
            caregiver_data = Caregiver.objects.create(**caregiver_data['caregiver'][0])

        if 'doctor' in validated_data['validated_data']:
            doctor_data = validated_data['validated_data'].pop('doctor')
            doctor_data = Doctor.objects.create(**doctor_data['doctor'][0])
        user = validated_data.pop('user')

        prescription = Prescription.objects.create(user=user, medicine=medicine_data, caregiver=caregiver_data,
                                           doctor=doctor_data)
        if 'subscriber' in validated_data['validated_data']:
            for value in validated_data['validated_data']['subscriber']:
                subscriber_obj = Subscriber.objects.create(subscriber_name=value['subscriber_name'])
                prescription.subscriber.add(subscriber_obj)
