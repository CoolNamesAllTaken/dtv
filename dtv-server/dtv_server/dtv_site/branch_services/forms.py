from django import forms
from django.forms import ModelForm # for TreatLicense
from branch_services.models import TreatLicense

class TreatLicenseForm(ModelForm):
    class Meta:
        model = TreatLicense
        fields = '__all__'