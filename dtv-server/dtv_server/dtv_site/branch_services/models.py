from django.db import models
from datetime import date

def get_treat_license_photo_path(instance, filename):
    # image will be uploaded to MEDIA_ROOT/treat_license_photos/{id}/John_M_2022101902.jpg
    return 'treat_license_photos/{}_{}_{}/{}-{}_{}-{}'.format(
        date.today().year,
        date.today().month,
        date.today().day,
        instance.license_number,
        instance.first_name,
        instance.costume_name,
        filename) # TODO: figure out if instance.id will work here

def get_new_license_number():
    day_count = (date.today() - date(1970, 1, 1)).days
    date_prefix = chr(ord('A') + int(day_count / 1e3)) # First letter is multiple of thousand days (this will fail in 20ish years)
    date_suffix = int(day_count % 1e3)
    license_counter = TreatLicense.objects.filter(issued_date=date.today()).count()
    return "{}{:03d}{:04d}".format(date_prefix, date_suffix, license_counter) # this will break something after 9999 licenses in one day!

def get_new_license_expiration_date():
    return date.today().replace(year=date.today().year + 1) # Treat license expires in one year

class TreatLicense(models.Model):
    TREAT_CLASS_ID_ONLY = 'ID'
    TREAT_CLASS_MMS = 'MM'
    TREAT_CLASS_REESES = 'RS'
    TREAT_CLASS_SKITTLES = 'SK'
    TREAT_CLASS_SNICKERS = 'SN'
    TREAT_CLASS_SOUR_PUNCH_STRAWS = 'SP'
    TREAT_CLASS_TWIX = 'TW'
    
    TREAT_CLASS_CHOICES = [
        (TREAT_CLASS_ID_ONLY, 'ID Card Only'),
        (TREAT_CLASS_MMS, 'M&Ms'),
        (TREAT_CLASS_REESES, 'Reeses'),
        (TREAT_CLASS_SKITTLES, 'Skittles'),
        (TREAT_CLASS_SNICKERS, 'Snickers'),
        (TREAT_CLASS_SOUR_PUNCH_STRAWS, 'Sour Punch Straws'),
        (TREAT_CLASS_TWIX, 'Twix')
    ]
    license_number = models.CharField(default=get_new_license_number, max_length=8, primary_key=True)
    first_name = models.CharField(max_length=32)
    costume_name = models.CharField(max_length=32)
    photo = models.FileField(upload_to=get_treat_license_photo_path, default='treat_license_photos/default/top_view.jpg')
    issued_date = models.DateField(default=date.today)
    expiration_date = models.DateField(default=get_new_license_expiration_date)
    treat_class = models.CharField(
        max_length = 2,
        choices = TREAT_CLASS_CHOICES,
        default = TREAT_CLASS_ID_ONLY,
        blank = False # Default to an ID card only class
    )
    treat_weight_oz = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    treat_length_in = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # TODO: add favorite number

    def get_wrapper_color(treat_class):
        """
        @brief Returns the wrapper color of a given candy type.
        @param[in] treat_class Two-letter treat class identifier.
        @retval Three-letter color identifier.
        """
        if treat_class is TREAT_CLASS_MMS:
            return 'BRN'
        elif treat_class is TREAT_CLASS_REESES:
            return 'ORN'
        elif treat_class is TREAT_CLASS_SKITTLES:
            return 'RED'
        elif treat_class is TREAT_CLASS_SNICKERS:
            return 'BRN'
        elif treat_class is TREAT_CLASS_SOUR_PUNCH_STRAWS:
            return 'GRN'
        elif treat_class is TREAT_CLASS_TWIX:
            return 'BRN'
        return 'WHT' # default and TREAT_CLASS_ID_ONLY
    
    def get_exterior_flavor(treat_class):
        """
        @brief Returns the exterior flavor of a given candy type.
        @param[in] treat class Two-letter treat class identifier.
        @retval Four-letter flavor identifier.
        """
        if treat_class is TREAT_CLASS_MMS:
            return 'SUGR'
        elif treat_class is TREAT_CLASS_REESES:
            return 'CHOC'
        elif treat_class is TREAT_CLASS_SKITTLES:
            return 'SUGR'
        elif treat_class is TREAT_CLASS_SNICKERS:
            return 'CHOC'
        elif treat_class is TREAT_CLASS_SOUR_PUNCH_STRAWS:
            return 'SOUR'
        elif treat_class is TREAT_CLASS_TWIX:
            return 'CHOC'
        return 'PLAS' # default and TREAT_CLASS_ID_ONLY

    def get_interior_flavor(treat_class):
        """
        @brief Returns the interior flavor of a given candy type.
        @param[in] treat class Two-letter treat class identifier.
        @retval Four-letter flavor identifier.
        """
        if treat_class is TREAT_CLASS_MMS:
            return 'CHOC' # various
        elif treat_class is TREAT_CLASS_REESES:
            return 'PNUT'
        elif treat_class is TREAT_CLASS_SKITTLES:
            return 'FRUT'
        elif treat_class is TREAT_CLASS_SNICKERS:
            return 'NOUG'
        elif treat_class is TREAT_CLASS_SOUR_PUNCH_STRAWS:
            return 'FRUT'
        elif treat_class is TREAT_CLASS_TWIX:
            return 'NOUG'
        return 'PLAS' # default and TREAT_CLASS_ID_ONLY
    
# TODO add nicer IDs for these two
class Ticket(models.Model):
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

class DtvWindow(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)
    available = models.BooleanField(default=True)