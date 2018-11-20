# Generated by Django 2.1.3 on 2018-11-18 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20181118_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='state',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='rider',
            name='state',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='state',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]