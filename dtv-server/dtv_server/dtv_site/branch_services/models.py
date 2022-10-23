from django.db import models
from datetime import date

def treat_license_photo_path(instance, filename):
    # image will be uploaded to MEDIA_ROOT/treat_license_photos/{id}/John_M_2022101902.jpg
    return 'treat_license_photos/{}_{}_{}/{}-{}_{}-{}'.format(
        date.today().year,
        date.today().month,
        date.today().day
        instance.id,
        instance.first_name,
        instance.last_initial,
        instance.filename) # TODO: figure out if instance.id will work here

class TreatLicenseCard(models.Model):
    first_name = models.CharField(max_length=32) # TODO: set these
    last_initial = models.CharField(max_length = 1)
    photo = models.FileField(upload_to=treat_license_photo_path)
    expiration_date = models.DateField(default=date.today().replace(year=date.today().year + 1)) # Treat license expires in one year
    treat_class = models.CharField(max_length=5)
    # treat_weight_oz = models.
    profession = models.CharField(max_length=32)
    favorite_color = models.CharField(max_length=4)
    favorite_animal = models.CharField(max_length=32)
    
