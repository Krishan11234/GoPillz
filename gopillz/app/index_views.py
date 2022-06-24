from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics


class Policy(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'terms_conditions.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class Monthly(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'GoPillz-yearly.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class UpdatePrescription(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'updateprescription.html'

    def get(self, request):
        content = {}
        return Response({'content': content})


class RenewSubscription(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'renewsubscription.html'

    def get(self, request):
        content = {}
        return Response({'content': content})