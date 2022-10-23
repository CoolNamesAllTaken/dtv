from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    return render(request, "branch_services/index.html")

def id_request(request):
    pass
