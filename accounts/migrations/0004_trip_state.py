# Generated by Django 2.1.3 on 2018-11-17 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_temptrip'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='state',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
