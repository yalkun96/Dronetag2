from django.db import models


class TelemetryMessage(models.Model):
    t_id = models.IntegerField(null=True)
    time = models.DateTimeField(null=True)
    time_recevied = models.DateTimeField(null=True)
    latitude = models.FloatField() #location
    longitude = models.FloatField() #location
    altitude = models.FloatField()
    geo_altitude = models.FloatField()
    height = models.FloatField()
    velocity_x = models.FloatField(help_text="X-component velocity in m/s")
    velocity_y = models.FloatField(help_text="Y-component velocity in m/s")
    velocity_z = models.FloatField(help_text="Z-component velocity in m/s")
    vertical_accuracy = models.FloatField()
    horizontal_accuracy = models.FloatField()
    speed_accuracy = models.FloatField()
    pressure = models.FloatField()


class StatusMessage(models.Model):
    s_id = models.IntegerField(null=True)
    time = models.DateTimeField(null=True)
    time_recevied = models.DateTimeField(null=True)
    battery = models.DecimalField(max_digits=5, decimal_places=2, help_text="Battery voltage in volts")
    cellid = models.CharField(max_length=200, help_text="ID of the current LTE cell station")
    rsrp = models.FloatField(help_text="Reference Signal Received Power of LTE in dBm")
    rsrq = models.FloatField(help_text="Reference Signal Received Quality of LTE in dB")
    snr = models.FloatField(help_text="Signal to Noise Ratio of LTE in dB")
    tac = models.CharField(max_length=100, help_text="Tracking Area Code of LTE")
    satellites = models.PositiveIntegerField(help_text="Number of visible GNSS satellites")
    charging = models.BooleanField(default=False, help_text="Indicates if the device is currently charging")
    flight_id = models.CharField(max_length=200, blank=True)




