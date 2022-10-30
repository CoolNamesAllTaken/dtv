from django.db import models
from datetime import date

from scripts.id_card_utils import assemble_id_card_image

import random # for choosing default photos
import os # for choosing default photots

"""Helper Functions (functions that are executed to create model field arguments)"""

def get_new_license_number():
    """
    @brief Generates a new license number based on the date and a sequential counter of number of licenses issued.
    """
    day_count = (date.today() - date(1970, 1, 1)).days
    date_prefix = chr(ord('A') + int(day_count / 1e3)) # First letter is multiple of thousand days (this will fail in 20ish years)
    date_suffix = int(day_count % 1e3)
    license_counter = TreatLicense.objects.filter(issued_date=date.today()).count()
    return "{}{:03d}{:04d}".format(date_prefix, date_suffix, license_counter) # this will break something after 9999 licenses in one day!

def create_id_card(instance):
    """
    @brief Generates ID card from a TreatLicense instance.
    @param[in] instance TreatLicense instance to harvest ID card data from.
    """
    assemble_id_card_image(
        output_path=instance.get_id_card_path(),
        license_number=instance.license_number,
        first_name=instance.first_name,
        costume_name=instance.costume_name,
        id_photo_path=instance.photo.name,
        issued_date="{}/{}/{}".format(instance.issued_date.month, instance.issued_date.day, instance.issued_date.year),
        expiration_date="{}/{}/{}".format(instance.expiration_date.month, instance.expiration_date.day, instance.expiration_date.year),
        treat_class=instance.treat_class,
        treat_weight="{} oz".format(instance.treat_weight_oz),
        treat_length="{} in".format(instance.treat_length_in),
        favorite_number="{}".format(instance.favorite_number),
        treat_wrapper_color=instance.get_wrapper_color(),
        treat_exterior_flavor=instance.get_exterior_flavor(),
        treat_interior_flavor=instance.get_interior_flavor(),
        issuer_code=instance.issuer_code
    )


"""Model Field Functions (functions that are passed as model field arguments)"""

def get_id_photo_path(instance, filename):
    """
    @brief Generates a filepath for a license photo.
    @param[in] self TreatLicense model instance.
    @param[in] filename 
    """
    # Image will be uploaded to MEDIA_ROOT/records/treat_license_photos/{license_number}/2022_10_19-image.jpg
    # Make all database filepaths forward slash separated for portability!
    return "records/treat_license_photos/{}_{}_{}/{}-id_card_photo-{}".format(
        instance.issued_date.year,
        instance.issued_date.month,
        instance.issued_date.day,
        instance.license_number,
        filename
    )

def get_random_default_photo_path():
    """
    @brief Returns the path to a random photo in the default ID card photos directory.
    @retval Path to a default photo, relative to MEDIA_ROOT.
    """
    default_photos_dir = "records/treat_license_photos/default"
    return "{}/{}".format(
        default_photos_dir,
        random.choice(os.listdir(default_photos_dir))
    )

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
    favorite_number = models.IntegerField()
    photo = models.ImageField(upload_to=get_id_photo_path, default=get_random_default_photo_path)
    issued_date = models.DateField(default=date.today)
    expiration_date = models.DateField(default=date.today().replace(year=date.today().year + 1)) # treat license expires in one year
    treat_class = models.CharField(
        max_length = 2,
        choices = TREAT_CLASS_CHOICES,
        default = TREAT_CLASS_ID_ONLY,
        blank = False # Default to an ID card only class
    )
    treat_weight_oz = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    treat_length_in = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    issuer_code = models.CharField(max_length=5)

    def get_wrapper_color(self):
        """
        @brief Returns the wrapper color of a given candy type.
        @retval Three-letter color identifier.
        """
        if self.treat_class == self.TREAT_CLASS_MMS:
            return 'BRN'
        elif self.treat_class == self.TREAT_CLASS_REESES:
            return 'ORN'
        elif self.treat_class == self.TREAT_CLASS_SKITTLES:
            return 'RED'
        elif self.treat_class == self.TREAT_CLASS_SNICKERS:
            return 'BRN'
        elif self.treat_class == self.TREAT_CLASS_SOUR_PUNCH_STRAWS:
            return 'GRN'
        elif self.treat_class == self.TREAT_CLASS_TWIX:
            return 'BRN'
        return 'WHT' # default and TREAT_CLASS_ID_ONLY
    
    def get_exterior_flavor(self):
        """
        @brief Returns the exterior flavor of a given candy type.
        @retval Four-letter flavor identifier.
        """
        if self.treat_class == self.TREAT_CLASS_MMS:
            return 'SUGR'
        elif self.treat_class == self.TREAT_CLASS_REESES:
            return 'CHOC'
        elif self.treat_class == self.TREAT_CLASS_SKITTLES:
            return 'SUGR'
        elif self.treat_class == self.TREAT_CLASS_SNICKERS:
            return 'CHOC'
        elif self.treat_class == self.TREAT_CLASS_SOUR_PUNCH_STRAWS:
            return 'SOUR'
        elif self.treat_class == self.TREAT_CLASS_TWIX:
            return 'CHOC'
        return 'PLAS' # default and TREAT_CLASS_ID_ONLY

    def get_interior_flavor(self):
        """
        @brief Returns the interior flavor of a given candy type.
        @retval Four-letter flavor identifier.
        """
        if self.treat_class == self.TREAT_CLASS_MMS:
            return 'CHOC' # various
        elif self.treat_class == self.TREAT_CLASS_REESES:
            return 'PNUT'
        elif self.treat_class == self.TREAT_CLASS_SKITTLES:
            return 'FRUT'
        elif self.treat_class == self.TREAT_CLASS_SNICKERS:
            return 'PCRM'
        elif self.treat_class == self.TREAT_CLASS_SOUR_PUNCH_STRAWS:
            return 'FRUT'
        elif self.treat_class == self.TREAT_CLASS_TWIX:
            return 'CRML'
        return 'PLAS' # default and TREAT_CLASS_ID_ONLY

    def get_id_card_path(self, ext="png"):
        """
        @brief Generates a filepath to the directory that contains treat license id files.
        @param[in] self TreatLicense model instance.
        """
        return "records/treat_license_id_card_files/{}/{}_{}_{}-id_card.{}".format(
            self.license_number,
            self.issued_date.year,
            self.issued_date.month,
            self.issued_date.day,
            ext
        )
    

