from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics
from django.contrib import messages
from django.shortcuts import redirect


class Policy(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'terms_conditions.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class HowItWorks(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'how_it_works.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class Yearly(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'GoPillz-yearly.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class UpdatePrescription(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'prescription.html'

    def get(self, request):
        if not request.user.is_authenticated:
            error_message = 'Before Payment Please Verify Who you are'
            messages.info(request, error_message)
            return redirect('/signup')
        content = {}
        return Response({'content': content})


class RenewSubscription(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'renewsubscription.html'

    def get(self, request):
        if not request.user.is_authenticated:
            error_message = 'Before Payment Please Verify Who you are'
            messages.info(request, error_message)
            return redirect('/signup')
        content = {}
        return Response({'content': content})