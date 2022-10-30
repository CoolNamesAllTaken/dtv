from django.contrib import admin
from .models import TreatLicense, DtvWindow, Ticket

# Register your models here.
admin.site.register(TreatLicense)
admin.site.register(DtvWindow)
admin.site.register(Ticket)
