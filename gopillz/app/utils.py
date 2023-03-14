import pyotp
from django.conf import settings
from twilio.rest import Client
from django.contrib.auth.models import User
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import string
import random


class Utils:
    def __init__(self, *args):
        self.email = args[0] if args else ''

    def generate_otp(self):
        totp = pyotp.TOTP('base32secret3232', interval=10)
        return totp.now()

    def generate_rand_string(self):
        res = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=200))
        return res

    def send_email_using_sendgrid(self, subject, context):
        import os
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=self.email,
            subject=subject,
            html_content=context
        )
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

    def send_sms_using_twilio(self, message, to):
        try:
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            print('-----------------------', message)
            message = client.messages \
                .create(
                    body=message,
                    from_=settings.MESSAGE_FROM,
                    to='+91' + str(to)
            )
            print(message.sid)
            return True
        except Exception as ex:
            return False


def create_staff_user(username, email, password):
    try:
        staff_user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password, is_staff=True,
                is_active=True, is_superuser=False)

        return staff_user
    except Exception as e:
        return None