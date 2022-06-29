from rest_framework import serializers
from .models import Plan, Payment, PaymentMethod


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('plan_type', 'price', 'duration')


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('method_name',)


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('user_id', 'payment_status', 'created', 'expired', 'exp_date', 'plan_id', 'payment_method_id')

    def create(self, validated_data):
        try:
            try:
                payment_data = Payment.objects.get(user_id=validated_data['user_id'])
            except Exception as e:
                payment_data = None

            if payment_data is not None:
                payment_data.payment_status = validated_data['payment_status']
                payment_data.plan_id = validated_data['plan_id']
                payment_data.payment_method_id = validated_data['payment_method_id']

                if validated_data['payment_status'] == 'complete':
                    payment_data.exp_date = validated_data['exp_date']
                    payment_data.created = validated_data['created']
                    payment_data.expired = validated_data['expired']
                    payment_data.renew = True
                else:
                    payment_data.expired = True
                    payment_data.renew = False

                payment_data.save()
            else:
                payment_data = Payment.objects.create(**validated_data)
                print(payment_data)
        except Exception as e:
            print(e)
            pass
