from rest_framework import routers, serializers,viewsets
from .models import Drone, Pilot

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ['serialNumber', 'positionY', 'positionX', 'lastUpdate']


class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pilot
        fields = '__all__'#['pilotId', 'firstName', 'lastName', 'phoneNumber', 'email', 'closestDistance','drone_id']

