# Generated by Django 4.0.2 on 2022-03-17 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_rename_date_articleheadline_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articleheadline',
            old_name='image',
            new_name='image_url',
        ),
    ]
