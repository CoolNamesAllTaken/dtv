from django import forms
from django.forms import ModelForm # for TreatLicense
from branch_services.models import TreatLicense, get_new_license_number

class TreatLicenseForm(ModelForm):
    class Meta:
        model = TreatLicense
        fields = '__all__'
    
    def clean_license_number(self):
        if self.cleaned_data.get('license_number') == "TBA":
            # Need to create a new license number.
            license_number = get_new_license_number()
            print("Assigning a new license number: {}.".format(license_number))
            return license_number
        print("License number {} was OK.".format(self.cleaned_data.get('license_number')))
        return self.cleaned_data.get('license_number')

class TreatLicenseLookupForm(forms.Form):
    license_number = forms.CharField(max_length=8, help_text="Enter the Treat License Number (TL) of the ID you would like to look up.")