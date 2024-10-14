from django.urls import path

from .views import receive_data, index,get_sensor_data,refresh,fresh_stop,get_refresh_data

urlpatterns = [
    path("", index, name="index"),
    path("receive-data/", receive_data, name="receive_data"),
    path("get-data/", get_sensor_data, name="get_sensor_data"),
    path("fresh/",refresh, name="ref"),
    path("fresh_stop/",fresh_stop, name="fresh_stop"),
    path("get_refresh_data/",get_refresh_data, name="get_refresh_data")
]
