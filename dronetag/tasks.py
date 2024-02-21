from celery import shared_task
from .models import TelemetryMessage

@shared_task
def process_telemetry_data(data):
    TelemetryMessage.objects.create(**data)