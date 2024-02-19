from django.db.models import Avg
from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from .models import *
from .serializer import *
import pandas as pd
import matplotlib.pyplot as plt
from asgiref.sync import sync_to_async
from threading import Thread
import plotly.express as px
import plotly.io as pio
import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np



def home(request):
    return render(request, 'dronetag/home.html')


class TelemetryMessageAPI(CreateAPIView):
    queryset = TelemetryMessage.objects.all()
    serializer_class = TelemetrySerializer


class StatusMessageAPI(CreateAPIView):
    queryset = StatusMessage.objects.all()
    serializer_class = StatusSerializer


def map_dashboard_view(request):
    telemetry_data = TelemetryMessage.objects.all()
    status_data = StatusMessage.objects.all()

    latitudes = [telemetry.latitude for telemetry in telemetry_data]
    longitudes = [telemetry.longitude for telemetry in telemetry_data]
    fig = px.scatter_mapbox(lat=latitudes, lon=longitudes, color_discrete_sequence=['#8500c2'], zoom=100, height=300,
                            width=600)

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=11,
        mapbox_center_lat=50.0755,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    map_html = fig.to_html()

    return render(request, 'dronetag/dashboard.html', {'map_html': map_html,
                                                       'telemetry_data': telemetry_data,
                                                       'status_data': status_data})



def link_reliability_dashboard(request):

    status_data = StatusMessage.objects.all()
    telemetry_data = TelemetryMessage.objects.all()

    average_data_altitude = []
    average_data_rsrp = []
    for cell_id in status_data.values_list('cellid', flat=True).distinct():
        filtered_data_status = status_data.filter(cellid=cell_id)
        avg_signal_strength = filtered_data_status.aggregate(avg_signal_strength=models.Avg('rsrp'))[
            'avg_signal_strength']
        average_data_rsrp.append(avg_signal_strength)

    for t_id in telemetry_data.values_list('t_id', flat=True).distinct():
        filtered_data_telemetry = telemetry_data.filter(t_id=t_id)
        avg_altitude = filtered_data_telemetry.aggregate(avg_altitude=models.Avg('altitude'))['avg_altitude']
        average_data_altitude.append(avg_altitude)

    average_data_altitude_last = average_data_altitude[-1]
    average_data_rsrp_last = average_data_rsrp[-1]

    status_data_fig = px.bar(status_data, x=[i.time for i in status_data],
                        y=[i.rsrp for i in status_data])

    telemetry_data_fig = px.bar(telemetry_data, x=[i.time for i in telemetry_data],
                      y=[i.altitude for i in telemetry_data])

    latency = status_data.last().time_recevied - telemetry_data.last().time_recevied

    if status_data:
        # Calculate metrics for link reliability analysis
        latency = status_data.last().time_recevied - telemetry_data.last().time_recevied  # Latency data
        packet_loss = status_data.last().rsrp
        signal_strength = status_data.last().rsrp

    if telemetry_data:
        telemetry_time_received_list = telemetry_data.order_by('time_recevied').values_list('time_recevied', flat=True)
        telemetry_arrival_intervals = np.diff(telemetry_time_received_list)

        telemetry_interval_fig = px.histogram(x=telemetry_arrival_intervals, nbins=20)
        telemetry_interval_fig.update_layout(title='Distribution of Telemetry Arrival Frequency Intervals',
                                             xaxis_title='Interval', yaxis_title='Frequency')

    if status_data:
        status_time_received_list = status_data.order_by('id').values_list('time_recevied', flat=True)
        status_arrival_intervals = np.diff(status_time_received_list)

        status_interval_fig = px.histogram(x=status_arrival_intervals, nbins=20)
        status_interval_fig.update_layout(title='Distribution of Status Arrival Frequency Intervals',
                                          xaxis_title='Interval', yaxis_title='Frequency')


    locations = telemetry_data.values_list('latitude', 'longitude').distinct()
    altitudes = telemetry_data.values_list('altitude').distinct()
    lte_cells = status_data.values_list('cellid').distinct()

    average_rsrp_by_cell = {}
    for cell in lte_cells:
        rsrp_values = status_data.filter(cellid=cell).values_list('rsrp', flat=True)
        average_rsrp_by_cell[cell] = sum(rsrp_values) / len(rsrp_values) if rsrp_values else 0




    status_html = status_data_fig.to_html()
    telemetry_html = telemetry_data_fig.to_html()
    telemetry_interval_html = telemetry_interval_fig.to_html
    status_interval_html = status_interval_fig.to_html()

    return render(request, 'dronetag/analysis.html', {'average_data_altitude_last': average_data_altitude_last,
                                                      'average_data_rsrp_last': average_data_rsrp_last,
                                                      'status_data': status_data,
                                                      'telemetry_data': telemetry_data,
                                                      'status_html': status_html,
                                                      'telemetry_html': telemetry_html,
                                                      'latency': latency,
                                                      'telemetry_interval_html': telemetry_interval_html,
                                                      'status_interval_html': status_interval_html,
                                                      'locations': locations,
                                                      'altitudes': altitudes,
                                                      'lte_cells': lte_cells,
                                                      'average_rsrp_by_cell': average_rsrp_by_cell

                                                      })



