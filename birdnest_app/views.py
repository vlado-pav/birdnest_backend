from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import DroneSerializer, PilotSerializer
from .models import Drone, Pilot
import datetime

@csrf_exempt
def drones(request):
    '''get method for all drones in the database in the past 10 minutes'''
    if request.method == 'GET':
        drones = Drone.objects.all()
        serializer = DroneSerializer(drones, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse('Bad request method, only "GET" is available.', status=400)

@csrf_exempt
def drones_actual(request):
    '''get method for drones in the database caught by radar in the last 2 seconds'''
    if request.method == 'GET':
        time_boundary = datetime.datetime.now() - datetime.timedelta(seconds=2.25)
        actual_drones = Drone.objects.filter(lastUpdate__gte=time_boundary)
        serializer = DroneSerializer(actual_drones, many=True)
        return JsonResponse(serializer.data, safe=False)
    else: 
        return JsonResponse('Bad request method, only "GET" is available.', status=400)

@csrf_exempt
def pilots(request):
    '''get method for all pilots from the table of pilots violating NDZ in the past 10 minutes'''
    if request.method == 'GET':
        pilots = Pilot.objects.all()
        serializer = PilotSerializer(pilots, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    else:
        return JsonResponse('Bad request method, only "GET" is available.', status=400)
