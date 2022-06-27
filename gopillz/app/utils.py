import pyotp
from django.conf import settings
from twilio.rest import Client


class Utils:
    def __init__(self, *args):
        self.email = ''

    def generate_otp(self):
        totp = pyotp.TOTP('base32secret3232', interval=10)
        return totp.now()

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

