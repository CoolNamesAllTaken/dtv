from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import TreatLicense

def index(request):
    num_treat_licenses = TreatLicense.objects.all().count()
    context = {
        'num_treat_licenses': num_treat_licenses
    }
    return render(request, "branch_services/index.html")

def id_request(request):
    pass
