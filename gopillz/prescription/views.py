from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import PrescriptionSerializer
from django.contrib import messages
from rest_framework.response import Response


class Prescription(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = PrescriptionSerializer
    template_name = "success.html"

    def post(self, request):
        request_data = self.prepare_request_data(request.data)
        prescription_serializer = self.serializer_class(data=request_data)
        response = Response()
        try:
            if prescription_serializer.is_valid(raise_exception=True):
                medicine_data = {}
                medicine_data['validated_data'] = prescription_serializer.validated_data
                medicine_data['user'] = request.user
                prescription_serializer.create(validated_data=medicine_data)
                error_message = 'Data Saved Successfully ADD Another'
                messages.success(request, error_message)
                response['status'] = True
                return response

            error_message = 'Validation Failed Check Data and Try again'
            messages.error(request, error_message)
            response['status'] = True
            return response

        except Exception as e:
            error_message = 'Validation Failed Check Data and Try again'
            if 'medicine' in e.args[0]:
                error_message = 'Medicine Type Cannot Blank'

            messages.error(request, error_message)
            response['status'] = True
            return response

    def prepare_request_data(self, data):
        request_data = {'medicine': [{}], 'doctor': [{}], 'caregiver': [{}]}
        subscriber_data = data.get('subscriber1', '')
        if len(subscriber_data) > 0:
            request_data['subscribers'].append(subscriber_data)
        subscriber_data = data.get('subscriber2', '')
        if len(subscriber_data) > 0:
            request_data['subscribers'].append(subscriber_data)
        subscriber_data = data.get('subscriber3', '')
        if len(subscriber_data) > 0:
            request_data['subscribers'].append(subscriber_data)
        subscriber_data = data.get('subscriber4', '')
        if len(subscriber_data) > 0:
            request_data['subscribers'].append(subscriber_data)

        if 'medicine_type' in data:
            request_data['medicine'][0]['medicine_name'] = ''
            request_data['medicine'][0]['medicine_type'] = data['medicine_type']
        if 'number_days' in data:
            request_data['medicine'][0]['medicine_name'] = ''
            request_data['medicine'][0]['number_days'] = data['number_days']
        if 'schedule_time' in data:
            request_data['medicine'][0]['medicine_name'] = ''
            request_data['medicine'][0]['schedule_time'] = data['schedule_time']
        if 'engagement' in data:
            request_data['medicine'][0]['medicine_name'] = ''
            request_data['medicine'][0]['level_of_engagement'] = data['engagement']
        if 'medicine_name' in data:
            request_data['medicine'][0]['medicine_name'] = data['medicine_name']

        if 'doctor_name' in data:
            request_data['doctor'][0]['doctor_name'] = data['doctor_name']
        if 'doctor_phone_no' in data:
            request_data['doctor'][0]['doctor_phone_no'] = '+91'+data['doctor_phone_no']
        if 'city' in data:
            request_data['doctor'][0]['city'] = data['city']
        if 'hospital_name' in data:
            request_data['doctor'][0]['hospital_name'] = data['hospital_name']
        if 'ailment' in data:
            request_data['doctor'][0]['Ailment'] = data['ailment']

        if 'caregiver_name' in data:
            request_data['caregiver'][0]['caregiver_name'] = data['caregiver_name']
        if 'phone_no' in data:
            request_data['caregiver'][0]['phone_no'] = '+91'+data['phone_no']
        if 'email' in data:
            request_data['caregiver'][0]['email'] = data['email']
        if 'relation' in data:
            request_data['caregiver'][0]['relation'] = data['relation']

        if len(request_data['medicine'][0].keys()) == 0:
            request_data.pop('medicine')
        if len(request_data['doctor'][0].keys()) == 0:
            request_data.pop('doctor')
        if len(request_data['caregiver'][0].keys()) == 0:
            request_data.pop('caregiver')

        return request_data
