# Generated by Django 5.0.2 on 2024-02-13 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dronetag', '0002_statusmessage_flight_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='telemetrymessage',
            name='flight_id',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
