from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import uuid
from . import ailment_types
# Create your models here.
phone_regex = RegexValidator(
        regex=r'^\+91\d{12}$', message="Phone number must be entered in the format: '+919999999999'. 10 digits allowed after +91."
    )

consent_storage_validator = RegexValidator(
        regex=r'^s3:.+$', message="Pincode must be 6 digits."
    )


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='patient_user')
    name = models.CharField(max_length=100)
    # TODO: should phone_number go to user and be here? or only user?
    phone_number = models.CharField(validators=[phone_regex], max_length=13, null=False)
    consent = models.BooleanField(null=False, default=False)
    # consent = models.CharField(max_length=1024, null=False, validators=[consent_storage_validator])
    # abha_id                     char? TODO
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_phone_number(self):
        return self.phone_number

    def get_preferred_family_member(self):
        return FamilyMember.objects.get(patient_fam=self)

    def get_preferred_family_name(self):
        return self.get_preferred_family_member().fam_name

    def get_preferred_family_number(self):
        return self.get_preferred_family_member().fam_number

    def get_name(self):
        return self.name

    def get_preferred_doctor(self):
        return DoctorPatient.objects.get(
            patient_doc=self,
            preferred=True,
            active=True
            )

    def get_preferred_doctor_name(self):
        doc_patient = self.get_preferred_doctor()
        doc_phone_numbers = DoctorPhoneNumbers.objects.get(
            doctor_reference=doc_patient.doctor_reference,
            number_type=1
        )
        return doc_phone_numbers.phone_number


class FamilyMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='family_user')
    patient_fam = models.ForeignKey(Patient, on_delete=models.CASCADE , null=True)
    fam_name = models.CharField(max_length=100)
    fam_number =  models.CharField(validators=[phone_regex], max_length=13, null=False)
    preferred = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#### TODO: move the remaining models to other apps
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='doctor_user')
    doctor_name = models.CharField(max_length=100, null=False)
    doctor_email = models.EmailField(null=True)
    speciality = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DoctorPhoneNumbers(models.Model):
    PHONE_NUMBER_TYPES = (
        (1, "Primary"),
        (2, "Assistant"),
        (3, "Booking Only"),
        (4, "TPA")
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=13, null=False)
    number_type =  models.CharField(max_length=100, choices=PHONE_NUMBER_TYPES, default=1)
    doctor_reference = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    #TODO: constraint that only one primary number can exist.


class DoctorPatient(models.Model):
    doctor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_doc = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor_reference = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)
    preferred = models.BooleanField(null=False, default=False)
    active = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class prescription -> not for now
# path_image
# ailment can be multiple
# medicine and lab tests
# stage of ailment?
    # these are fixed, but different for each ailment


class Medicine(models.Model):
    med_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patiend_med = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    med_name = models.CharField(max_length=100, default=None, null=True)
    duration = models.IntegerField(default=None, null=True)
    # days_of_week = models.CharField(max_length=100)
    active = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Doses(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    med_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MedicineDay(models.Model):
    NUMBER_DAYS = (
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    )
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    days_of_week = models.CharField(max_length=100,  choices=NUMBER_DAYS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ailment(models.Model):
    ailment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_ailment = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    ailment_type = models.CharField(max_length=100, choices=ailment_types.AILMENT_TYPES) # need to add choices
    ailment_other_type = models.CharField(max_length=100, default=None, null=True)
    active = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

##TODO: add a model manager for hospital, doctor, etc.
# hospital/lab
# name
# # of branches
# get key doctors -> well known & high revenue #TODO: add this field
# get locations
# specialities
#

# lab
# keep test list for later


class Hospital(models.Model):
    hospital_name = models.CharField(max_length=100)
    url = models.URLField(max_length=50, null=True)
    email = models.EmailField(null=True)
    # logo? TODO: add this field
    parent_company_name = models.CharField(max_length=100, default=None, null=False) # TODO: add choices for this
    display = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class HospitalPhoneNumbers(models.Model):
    PHONE_NUMBER_TYPES = (
        (1, "Primary"),
        (2, "Assistant"),
        (3, "Booking Only"),
        (4, "TPA")
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=13, null=False)
    number_type = models.CharField(max_length=100, choices=PHONE_NUMBER_TYPES, default=1)
    hospital_reference = models.ForeignKey(Hospital, on_delete=models.CASCADE)


class HospitalPatient(models.Model):
    hos_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_hospital = models.ForeignKey(Patient, on_delete = models.CASCADE, null=True)
    hospital_reference = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=False)
    preferred = models.BooleanField(null=False, default=False)
    active = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Chemist(models.Model):
     # most of the choices here are not critical except to distinguish MR from
     # a regular chemist. Other choices have been added in case the data is useful
     # later. However, this can be collapsed to choices 1 and 2 if needed.
    CHEMIST_TYPES = (
        (1, "Individual Chemist"),
        (2, "Medical Representative"),
        (3, "Hospital Chemist"),
        (4, "Chemist Chain Branch")
    )
    chemist_name = models.CharField(max_length=100)
    chemist_type = models.CharField(max_length=255, null=False, choices=CHEMIST_TYPES)
    url = models.URLField(max_length=50, null=True)
    email = models.EmailField(null=True)

    display = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChemistPhoneNumbers(models.Model):
    PHONE_NUMBER_TYPES = (
        (1, "Primary"),
        (2, "Assistant"),
        (3, "Booking Only"),
        (4, "TPA")
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=13, null=False)
    number_type =  models.CharField(max_length=100, choices=PHONE_NUMBER_TYPES, default=1)
    chemist_reference = models.ForeignKey(Chemist, on_delete=models.CASCADE)


class ChemistPatient(models.Model):
    chemist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_chemist = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    chemist_reference = models.ForeignKey(Chemist, on_delete=models.CASCADE, null=False)
    preferred = models.BooleanField(null=False, default=False)
    active = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Lab(models.Model):
    lab_name = models.CharField(max_length=100)
    url = models.URLField(max_length=50, null=True)
    email = models.EmailField(null=True)
    display = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LabPatient(models.Model):
    lab_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_lab = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    lab_reference = models.ForeignKey(Lab, on_delete=models.CASCADE, null=False)
    preferred = models.BooleanField(null=False, default=False)
    active = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LabPhoneNumbers(models.Model):
    PHONE_NUMBER_TYPES = (
        (1, "Primary"),
        (2, "Assistant"),
        (3, "Booking Only"),
        (4, "TPA")
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=13, null=False)
    number_type =  models.CharField(max_length=100, choices=PHONE_NUMBER_TYPES, default=1)
    lab_reference = models.ForeignKey(Lab, on_delete=models.CASCADE)
    active = models.BooleanField(null=False, default=False) # TODO: decide if active is needed in phone numbers?


class Ambulance(models.Model):
    ambulance_name = models.CharField(max_length=100)
    ambulance_number = models.CharField(validators=[phone_regex], max_length=13, null=False)
    url = models.URLField(max_length=50, null=True)
    email = models.EmailField(null=True)
    # display       bool
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AmbulancePatient(models.Model):
    ambulance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_ambulance = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    ambulance_reference = models.ForeignKey(Ambulance, on_delete=models.CASCADE, null=False)
    preferred = models.BooleanField(null=False, default=False)
    active = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AmbulancePhoneNumbers(models.Model):
    PHONE_NUMBER_TYPES = (
        (1, "Primary"),
        (2, "Assistant"),
        (3, "Booking Only"),
        (4, "TPA")
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=13, null=False)
    number_type =  models.CharField(max_length=100, choices=PHONE_NUMBER_TYPES, default=1)
    ambulance_reference = models.ForeignKey(Ambulance, on_delete=models.CASCADE)
    active = models.BooleanField(null=False, default=False)