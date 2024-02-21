from django.test import TestCase
from django.urls import reverse
from .models import TelemetryMessage, StatusMessage
from .tasks import process_telemetry_data


class TelemetryMessageModelTestCase(TestCase):
    def test_telemetry_message_creation(self):
        telemetry = TelemetryMessage.objects.create(
            latitude=42.1234,
            longitude=-71.5678,
            altitude=100,
            geo_altitude=200,
            height=300,
            velocity_x=0,
            velocity_y=0,
            velocity_z=0,
            horizontal_accuracy=10,
            vertical_accuracy=10,
            speed_accuracy=10,
            pressure=1013.25,
        )
        self.assertEqual(telemetry.latitude, 42.1234)
        self.assertEqual(telemetry.longitude, -71.5678)
        self.assertEqual(telemetry.altitude, 100)


class StatusMessageModelTestCase(TestCase):
    def test_status_message_creation(self):
        status = StatusMessage.objects.create(
            battery=3.5,
            cellid="LTE123",
            rsrp=-80,
            rsrq=-90,
            snr=-70,
            satellites=10,

        )
        self.assertEqual(status.battery, 3.5)
        self.assertEqual(status.cellid, "LTE123")
        self.assertEqual(status.rsrp, -80)

