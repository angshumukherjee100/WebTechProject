# Generated by Django 2.1.3 on 2018-11-19 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_driver_lastlocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='lastLocation',
            field=models.CharField(choices=[('ap', 'Airport'), ('ba', 'Baguiati'), ('lt', 'Lake Town'), ('bg', 'Beleghata'), ('rh', 'Ruby Hospital')], default='ba', max_length=100, null=True),
        ),
    ]
