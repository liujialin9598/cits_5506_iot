from django.urls import path

from .views import receive_data, index,get_sensor_data

urlpatterns = [
    path("", index, name="index"),
    path("receive-data/", receive_data, name="receive_data"),
    path("get-data/", get_sensor_data, name="get_sensor_data"),
]
