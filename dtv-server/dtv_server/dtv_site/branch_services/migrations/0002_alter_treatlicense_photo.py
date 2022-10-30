# Generated by Django 4.1.2 on 2022-10-30 01:30

import branch_services.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch_services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatlicense',
            name='photo',
            field=models.ImageField(default=branch_services.models.get_random_default_photo_path, upload_to=branch_services.models.get_id_photo_path),
        ),
    ]
