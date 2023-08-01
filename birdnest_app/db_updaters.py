import xmltodict
from .serializers import DroneSerializer, PilotSerializer
from .models import Drone, Pilot
import datetime
import requests
from json import loads
from math import sqrt
from . import config

def update_databases():
    '''This function is called from APScheduler to run every 2s. It should update the table of drones and pilots (if necessary)
    Also, removes old drones, as only drones from the last ten minutes need to be persistent.'''
    
    now = datetime.datetime.now()

    update_drones(now)
    delete_old_drones_and_pilots(now,treshold=datetime.timedelta(seconds=config.DELETION_TIME_TRESHOLD))

def get_pilot(drone_serial_number:str) -> dict:  
    '''get pilot from the remote API based on the drone's serial number'''

    r = requests.get('https://assignments.reaktor.com/birdnest/pilots/'+drone_serial_number)
    return loads(r.content)

def get_drones() -> dict:
    '''get drones from the remote API'''

    r = requests.get('https://assignments.reaktor.com/birdnest/drones')
    return xmltodict.parse(r.content)['report']['capture']['drone']

def delete_old_drones_and_pilots(time:datetime.datetime, treshold:datetime.timedelta) -> None: 
    '''Deletes drones and pilots (cascading) older than treshold limit'''

    last_allowed = time - treshold
    old_drones = Drone.objects.filter(lastUpdate__lte=last_allowed)
    for drone in old_drones:
        drone.delete()

def update_current_drone(drone, time:datetime) -> None:
    '''If the given drone exists, update its position; else create new drone in the db'''

    #Get the drone object
    filtered = Drone.objects.filter(serialNumber=drone['serialNumber'])    
    if filtered: #if exists
        filtered.update(positionX=drone['positionX'], positionY=drone['positionY'],lastUpdate=time)

    else: 
        #If the drone does not exist, create one, validate and save into db
        drone['lastUpdate'] = time
        serializer = DroneSerializer(data=drone)
        if serializer.is_valid():
            serializer.save()

def update_drones(time:datetime):
    '''The main function for updating drones and pilots tables in db.
    First, the function gets actual drones from remote API and updates Drones table accordingly.
    Second, checks, if the drone is violating NDZ. If violating, update pilot info in db.
    '''

    current_drones = get_drones() 
    for drone in current_drones:
        update_current_drone(drone,time)

        #check if drone is violating NDZ
        distance = sqrt((float(drone['positionX'])-config.SENSOR_POSITION_X)**2 + (float(drone['positionY'])-config.SENSOR_POSITION_Y)**2)

        if distance <= config.NDZ_RADIUS:
            #check if pilot has already been added into db
            pilot_in_db = Pilot.objects.filter(drone=drone['serialNumber'])
            if not pilot_in_db:
                #Try adding the pilot to the db
                #'Try-Except' method only due to the statement in assignment: "Please note on a rare occasion pilot information may not be found, indicated by a 404 status code."
                try:
                    pilot = get_pilot(drone['serialNumber'])

                    del pilot['createdDt']
                    pilot['closestDistance'] = distance
                    pilot['lastAppearance'] = time
                    pilot['drone'] = drone['serialNumber']

                    serializer = PilotSerializer(data=pilot)
                    if serializer.is_valid():
                        serializer.save()

                except:
                    #simply not adding this pilot into db
                    pass
            else:
                #if pilot is in db, only update 'closestDistance' if necessary
                old_closest_distance = pilot_in_db.values()[0]['closestDistance']
                if old_closest_distance > distance:
                    pilot_in_db.update(closestDistance=distance)
