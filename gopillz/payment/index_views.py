from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Payment, Plan
from .serializers import PlanSerializer
from django.conf import settings


class RenewSubscription(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'renewsubscription.html'
    upgrade_template_name = 'upgrade-subscription.html'
    plan_format = {
        'couple': 'Couple',
        'single': 'Single',
        'family_friends': 'Family&Friends',
    }

    def get(self, request):
        content = {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY_TEST}
        if not request.user.is_authenticated:
            error_message = 'Please sign up to purchase plan'
            messages.info(request, error_message)
            return redirect('/signup')
        try:
            try:
                subscription_data = Payment.objects.get(user_id=request.user.id)
            except Exception as e:
                info_message = 'No Payment Has Been made Please select plan'
                messages.info(request, info_message)
                return redirect('/payment')
            if subscription_data.expired:
                info_message = 'Your Subscription Has been Expired'
                messages.info(request, info_message)
            content['plan_type'] = self.plan_format[subscription_data.plan.plan_type]
            content['price'] = subscription_data.plan.price
            content['duration'] = subscription_data.plan.duration

        except Exception as e:
            pass
        if request.query_params.get('upgrade','')=='True':
            plans = Plan.objects.all()
            plan_serializer = PlanSerializer(plans, many=True)
            content['plans'] = []
            try:
                for plan in plan_serializer.data:
                    temp_plan_row = {}
                    temp_plan_row['plan_type'] = plan['plan_type']
                    temp_plan_row['plan_name'] = self.plan_format[plan['plan_type']]
                    temp_plan_row['duration'] = plan['duration']
                    temp_plan_row['price'] = plan['price']
                    content['plans'].append(temp_plan_row)

                content['active_plan'] = request.query_params.get('val', 'yearly')
                return render(request, self.upgrade_template_name, {'content': content})
            except Exception as e:
                info_message = 'Cannot Upgrade Subscription at this moment Try After Some Time'
                messages.error(request, info_message)
        return Response({'content': content})


class Proceed(generics.GenericAPIView):
    def get(self, request):
        info_message = 'Cannot Proceed From here without Upgrading plan'
        messages.info(request, info_message)
        return redirect('/renew-subscription')