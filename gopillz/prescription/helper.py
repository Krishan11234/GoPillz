import datetime

MEDICINE_TYPE = (
    ("adhesive", "adhesive(s)"),
    ("capsule", "capsule(s)"),
    ("cachet", "cachet(s)"),
    ("cream", "cream(s)"),
    ("dragee", "dragee(s)"),
)

NUMBER_DAYS = (
    ("1", "Monday"),
    ("2", "Tuesday"),
    ("3", "Wednesday"),
    ("4", "Thursday"),
    ("5", "Friday"),
    ("6", "Saturday"),
    ("7", "Sunday"),
)

SCHEDULE_TIME = (
    ("1", "Before Breakfast - Simastatin"),
    ("2", "After Breakfast - Loratadine"),
    ("3", "Before Lunch - Montelukast)"),
    ("4", "After Lunch - Simvastatin"),
    ("5", "Before Dinner - Loratadine"),
)

LEVEL_ENGAGEMENT = (
    ("1", "Daily - Morning and Evening"),
    ("2", "Daily - Morning, Lunch, Evening, Dinner"),
    ("3", "As per prescription"),
)


def get_email_verified_data(user):
    from .models import EmailVerification
    data = None
    email_verify = EmailVerification.objects.filter(user=user)
    if email_verify:
        data = email_verify[0]
    return data