from django.db import models

# Create your models here.

class Drone(models.Model):
    serialNumber = models.CharField(max_length=32, primary_key=True)
    positionY = models.FloatField()
    positionX = models.FloatField()
    lastUpdate = models.DateTimeField()

    class Meta:
        ordering = ['lastUpdate']
    
    def __str__(self):
        return self.serialNumber

class Pilot(models.Model):
    pilotId = models.CharField(max_length=32, primary_key=True)
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    phoneNumber = models.CharField(max_length=64)
    email = models.CharField(max_length=128)
    lastAppearance = models.DateTimeField()
    closestDistance = models.FloatField(blank=True)
    drone = models.ForeignKey(Drone, db_column='serialNumber', on_delete=models.CASCADE) #ForeignKey(Drone, db_column='serialNumber', related_name='pilot', on_delete=models.CASCADE)
    #drone = models.CharField(max_length=32)
    def __str__(self):
        return self.firstName + ' ' + self.lastName

    class Meta:
        ordering = ['closestDistance']