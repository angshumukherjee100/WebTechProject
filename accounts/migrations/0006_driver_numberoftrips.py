# Generated by Django 2.1.3 on 2018-11-17 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_trip_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='numberOfTrips',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
