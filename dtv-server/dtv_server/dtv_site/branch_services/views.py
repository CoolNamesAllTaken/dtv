from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
import random
import json
from .models import TreatLicense, get_new_license_number, DtvWindow, Ticket
from branch_services.forms import TreatLicenseForm

def index(request):
    num_treat_licenses = TreatLicense.objects.all().count()
    context = {
        'num_treat_licenses': num_treat_licenses
    }
    return render(request, "branch_services/index.html")

def create_id(request):
    # treat_license = get_object_or_404(TreatLicense, pk=get_new_license_number())

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = TreatLicenseForm(request.POST, request.FILES)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            form.save()

            # redirect to a new URL:
            return HttpResponseRedirect('edit_id/' + form.cleaned_data['license_number'] + '/success')

    # If this is a GET (or any other method) create the default form.
    else:
        form = TreatLicenseForm()

    context = {
        'form': form,
        'form_title': "DTV ID Creator",
        'form_success_banner_display': "d-none"
    }

    return render(request, "branch_services/id_editor.html", context)

def edit_id(request, license_number, slug=None):
    treat_license = get_object_or_404(TreatLicense, pk=license_number)
    print(slug)
    if (slug == "success"):
        display_form_success_banner = True # came here from a successful operation
    else:
        display_form_success_banner = False

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = TreatLicenseForm(request.POST, request.FILES, instance=treat_license)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            treat_license.save()
            display_form_success_banner = True
            # hop on down to the render

    # If this is a GET (or any other method) create the default form.
    else:
        form = TreatLicenseForm(instance=treat_license)

    if display_form_success_banner:
        form_success_banner_display_style = ""
    else:
        form_success_banner_display_style = "d-none"
    context = {
        'form': form,
        'form_title': "DTV ID Editor",
        'form_success_banner_display': form_success_banner_display_style
    }

    return render(request, "branch_services/id_editor.html", context)


def status(request):
    windows = DtvWindow.objects.all()
    context = {
        'windows': windows
    }
    return render(request, "branch_services/status.html", context)


def get_window_status(request):
    windows = DtvWindow.objects.all().order_by('-ticket__datetime_created')
    context = {
        'windows': [window.id for window in windows],
        'tickets': [window.ticket.id if window.ticket is not None else '-' for window in windows],
    }
    return JsonResponse(context)

    
def window(request, window_number):
    current_window = get_object_or_404(DtvWindow, pk=window_number)
    context = {
        'window_number': window_number,
        'current_ticket': current_window.ticket.id if current_window.ticket is not None else '-'
    }
    return render(request, "branch_services/window.html", context)

def get_new_ticket(request):
    ticket_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    ticket_count = Ticket.objects.count()
    ticket_id = ticket_letter + str(ticket_count).zfill(3)
    ticket = Ticket(id=ticket_id, completed=False)
    ticket.save()
    ticket_info = {'ticketNumber': ticket_id}
    return JsonResponse(ticket_info)

def get_next_ticket(request):
    print(request.body)
    tickets = Ticket.objects.filter(completed=False).filter(dtvwindow__isnull=True).order_by('-datetime_created')
    next_ticket = tickets[0]
    window = DtvWindow.objects.get(id=json.loads(request.body)['window_number'])
    if window.ticket.completed:
        window.ticket = next_ticket
        window.save()
        ticket_info = {'ticketNumber': next_ticket.id}
    else:
        ticket_info = {'ticketNumber': window.ticket.id}
    return JsonResponse(ticket_info)

def complete_ticket(request):
    print(request.body)
    window = DtvWindow.objects.get(id=json.loads(request.body)['window_number'])
    window.ticket.completed = True
    window.ticket.save()
    ticket_info = {'ticketNumber': '-'}
    return JsonResponse(ticket_info)

def create_ticket(request):
    return render(request, "branch_services/create_ticket.html")