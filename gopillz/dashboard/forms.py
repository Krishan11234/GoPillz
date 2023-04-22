from django import forms
from prescription.models import Subscriber


class PaymentLinkForm(forms.ModelForm):
    name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        print("My custom admin Form")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Subscriber
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(),
        }