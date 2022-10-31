from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.conf import settings # for MEDIA_ROOT etc

from .models import TreatLicense, get_new_license_number, create_id_card, DtvWindow
from branch_services.forms import TreatLicenseForm, TreatLicenseLookupForm

from scripts import id_card_utils

def create_id_card_from_form(form):
    form.save() # update the TreatLicense model in the database with new info

    # Build and save an ID card
    license_number = form.cleaned_data['license_number']
    treat_license = get_object_or_404(TreatLicense, pk=license_number)
    create_id_card(treat_license)

def index(request):
    try:
        latest_treat_license = TreatLicense.objects.latest('license_number')
        id_card_image_data = id_card_utils.encode_id_card_image(latest_treat_license.get_id_card_path())
    except:
        id_card_image_data = ""
    context = {
        'num_ids_created': TreatLicense.objects.all().count(),
        'id_card_image_data': id_card_image_data
    }
    return render(request, "branch_services/index.html", context)

def edit_id(request, license_number=None):
    """
    @brief View used for editing a TreatLicense ID card.
    @param[in] request HTTP request for the page (GET for accessing, POST when submitting the form).
    @param[in] license_number String containing unique ID of license to edit.
    @param[in] slug Additional arguments passed via URL. Used to denote landing on this page from the create_id view via the "success" slug.
    @retval Rendered HTML.
    """
    if license_number:
        # Editing an existing license
        treat_license = get_object_or_404(TreatLicense, pk=license_number)
        id_card_image_data = id_card_utils.encode_id_card_image(treat_license.get_id_card_path())
        form_title = "Edit Existing ID Card"
    else:
        # Creating a new license
        treat_license = None
        id_card_image_data = id_card_utils.encode_id_card_image("scripts/assets/dtv_card_front_600dpi.png")
        form_title = "Create New ID Card"

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = TreatLicenseForm(request.POST, request.FILES, instance=treat_license)
        # Not for human consumption, since the only way the user sees this form is if the form is not valid even though it was POSTed.
        # Disable the sensitive fields anyways, just to be safe.
        form.fields['license_number'].disabled = True
        # form.fields['license_number'].required = False

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            create_id_card_from_form(form)

            # redirect to a new URL:
            return HttpResponseRedirect('/branch_services/edit_id/' + form.cleaned_data['license_number'])

    # If this is a GET (or any other method) create the default form.
    else:
        form = TreatLicenseForm(instance=treat_license)
        # Don't allow the user to touch the license number field to avoid conflicts.
        form.fields['license_number'].disabled = True
        # Allow any random ass garbage to be submitted 
        # form.fields['license_number'].required = False

    if treat_license:
        # Treat license exists, enable print function and "New ID" button.
        existing_id_banner_display_style = ""
        license_number = treat_license.license_number
    else:
        existing_id_banner_display_style = "d-none"
        license_number = "None"
    
    context = {
        'form': form,
        'form_title': form_title,
        'existing_id_banner_display': existing_id_banner_display_style,
        'id_card_image_data': id_card_image_data,
        'license_number': license_number
    }

    return render(request, "branch_services/id_editor.html", context)

def status(request):
    windows = DtvWindow.objects.all()
    context = {
        'windows': windows
    }
    return render(request, "branch_services/status.html", context)


def get_window_status(request):
    windows = DtvWindow.objects.all()
    context = {
        'windows': [window.id for window in windows],
        'tickets': [window.ticket.id if window.ticket is not None else '-' for window in windows],
    }
    return JsonResponse(context)
    
def print_id(request, license_number):
    """
    @brief Endpoint used for triggering print jobs of TreatLicense ID cards.
    @param[in] request HTTP request. POST to trigger a print, others rejected.
    @param[in] license_number Unique ID of TreatLicense to print.
    @retval JsonResponse dictionary with success and error_msg fields.
    """
    response_dict = {
        'success': False,
        'error_msg': ""
    }
    if request.method == 'POST':
        # Someone is trying to send a print job.
        try:
            treat_license = get_object_or_404(TreatLicense, pk=license_number)
        except:
            response_dict['error_msg'] = "Could not find TreatLicense with license number {}".format(license_number)
            return JsonResponse(response_dict)

        try:
            id_card_utils.print_id_card(settings.MEDIA_ROOT + "/" + treat_license.get_id_card_path(ext="pdf"))
        except Exception as e:
            response_dict['error_msg'] = "Failed to print ID card with exception: {}.".format(e)
            return JsonResponse(response_dict)
        
        response_dict['success'] = True
       
    else:
        # Reject everything that isn't a POST request.
        response_dict['error_msg'] = "Not a POST request."

    return JsonResponse(response_dict)

def lookup_id(request):
    message = "Lookup ID by license number."
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = TreatLicenseLookupForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            license_number = form.cleaned_data['license_number']
            try:
                treat_license = get_object_or_404(TreatLicense, pk=license_number)
                # redirect to a new URL:
                return HttpResponseRedirect('/branch_services/edit_id/' + license_number)
            except:
                message = "ID number {} not found!".format(license_number)
        else:
            message = "Form contents not valid. Try again!"
    else:
        form = TreatLicenseLookupForm()
    
    context = {
        'form': form,
        'message': message
    }
    
    return render(request, "branch_services/id_lookup.html", context)
