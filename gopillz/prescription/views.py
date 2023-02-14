from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import SubscribeSerializer
from django.contrib import messages
from rest_framework.response import Response
from datetime import datetime
from django.http import JsonResponse


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
                subscriber_serializer.save_record(validated_data=subscriber_serializer.validated_data, user=request.user)
                message = "Subscriber Successfully added"
                return JsonResponse({
                    'message': message,
                    'status': 'info'
                })

        except Exception as e:
            error_message = ' Failed Check Data and Try again'
            if 'phone_number' in e.args[0]:
                error_message = str(e.args[0]['phone_number'][0])

            return JsonResponse({
                'message': error_message,
                'status': 'danger'
            })

    def prepare_request_data(self, data):
        request_data = {}
        try:
            subscriber_name = data.get('subscriber_name', '')
            if len(subscriber_name) > 0:
                request_data['subscriber_name'] = subscriber_name

            phone_number = data.get('phone_no', '')
            if len(phone_number) > 0:
                request_data['phone_number'] = '+91'+phone_number

            address = data.get('address', '')
            if len(address) > 0:
                request_data['address'] = address

            city = data.get('city', '')
            if len(city) > 0:
                request_data['city'] = city

            country = data.get('country', '')
            if len(country) > 0:
                request_data['country'] = country

            pin_code = data.get('pin_code', '')
            if len(pin_code) > 0:
                request_data['pin_code'] = int(pin_code)
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


class PrescriptionView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "prescription.html"

    def get(self, request, *args, **kwargs):
        info_message = 'Payment Processing Completed'
        messages.info(request, info_message)
        return Response({
            'content': "",
        })