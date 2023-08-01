from django.urls import path
from . import views

urlpatterns = [
    path('drones', views.drones),
    path('drones_actual', views.drones_actual),
    path('pilots', views.pilots),
]
