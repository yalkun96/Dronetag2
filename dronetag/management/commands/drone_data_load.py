from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from itertools import islice
from django.conf import settings
from dronetag.models import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.status_script()
        self.telemetry_script()

    def status_script(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'data' / 'status_data.csv'

        with open(datafile, 'r') as status_data:
            reader = csv.DictReader(islice(status_data, 0, None))

            for row in reader:
                StatusMessage.objects.get_or_create(
                    s_id=row['id'],
                    time=row['time'],
                    time_recevied=row['time_received'],
                    battery=float(row['battery']),
                    cellid=row['cellid'],
                    rsrp=float(row['rsrp']),
                    rsrq=float(row['rsrq']),
                    snr=float(row['snr']),
                    tac=row['tac'],
                    satellites=int(row['satellites']),
                    charging=row['charging'] == 'True',



                )

    def telemetry_script(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'data' / 'telemetry_data.csv'

        with open(datafile, 'r') as telemetry_data:
            reader = csv.DictReader(islice(telemetry_data, 0, None))

            for row in reader:
                TelemetryMessage.objects.get_or_create(
                    t_id=row['id'],
                    time=row['time'],
                    time_recevied=row['time_received'],
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    altitude=float(row['altitude']),
                    geo_altitude=float(row['geo_altitude']),
                    height=float(row['height']),
                    velocity_x=float(row['velocity_x']),
                    velocity_y=float(row['velocity_y']),
                    velocity_z=float(row['velocity_z']),
                    vertical_accuracy=float(row['vertical_accuracy']),
                    horizontal_accuracy=float(row['horizontal_accuracy']),
                    speed_accuracy=float(row['speed_accuracy']),
                    pressure=float(row['pressure'])
                )