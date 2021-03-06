# Generated by Django 2.1.3 on 2018-11-15 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181115_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='tempTrip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fare', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, null=True)),
                ('fromLocation', models.CharField(choices=[('ap', 'Airport'), ('ba', 'Baguiati'), ('lt', 'Lake Town'), ('bg', 'Beleghata'), ('rh', 'Ruby Hospital')], max_length=150, null=True)),
                ('toLocation', models.CharField(choices=[('ap', 'Airport'), ('ba', 'Baguiati'), ('lt', 'Lake Town'), ('bg', 'Beleghata'), ('rh', 'Ruby Hospital')], max_length=150, null=True)),
                ('driverID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.driver')),
                ('riderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.rider')),
            ],
        ),
    ]
