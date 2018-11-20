from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

from django.conf import settings

class customUser(AbstractUser):
	pass

class rider(models.Model):
	phone = models.PositiveIntegerField(unique = True, null = True, blank = False)
	name = models.CharField(max_length = 150, null = True, blank = False)
	email = models.EmailField(max_length = 100, null = True, blank = False, unique = True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, unique = True)
	state = models.PositiveIntegerField(null = True, blank = False, default = 0)	#state = 0 for free, 1 for riding

class driver(models.Model):
	CAR_TYPE = (('eco','Economic'),('prem','Premium'),('suv','SUV'))
	LOCATION_CHOICES = (('ap', 'Airport'), ('ba', 'Baguiati'), ('lt', 'Lake Town'), ('bg', 'Beleghata'), ('rh', 'Ruby Hospital'))
	phone = models.PositiveIntegerField(unique = True, null = True, blank = False)
	name = models.CharField(max_length = 150, null = True, blank = False)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, unique = True)
	email = models.EmailField(max_length = 100, null = True, blank = False, unique = True)
	license = models.CharField(max_length = 150, null = True, blank = False)
	vehicleName = models.CharField(max_length = 150, null = True, blank = False)
	state = models.PositiveIntegerField(null = True, blank = False, default = 0)	#state = 0 for free, 1 for reviewingTrip, 2 for driving 
	vehicleNumber = models.CharField(max_length = 150, null = True, blank = False)
	rating = models.PositiveIntegerField(default= 0,null = True,  blank = True)
	carType = models.CharField(max_length = 100, choices = CAR_TYPE, null = True)
	numberOfTrips = models.PositiveIntegerField(null = True, blank = False, default = 0)
	lastLocation = models.CharField(max_length = 100, choices = LOCATION_CHOICES, null = True, default = LOCATION_CHOICES[random.randint(0,4)][0])

class trip(models.Model):
	LOCATION_CHOICES = (('ap', 'Airport'), ('ba', 'Baguiati'), ('lt', 'Lake Town'), ('bg', 'Beleghata'), ('rh', 'Ruby Hospital'))
	startTime = models.DateTimeField(default = None, null = True)
	endTime = models.DateTimeField(default = None, null = True)
	fare = models.DecimalField(decimal_places = 2, max_digits = 5, null = True, default = 0.0, blank = True)
	fromLocation = models.CharField(max_length = 150, null = True, blank = False, choices = LOCATION_CHOICES)
	toLocation = models.CharField(max_length = 150, null = True, blank = False, choices = LOCATION_CHOICES)
	riderID = models.ForeignKey(rider, on_delete = models.CASCADE)
	driverID = models.ForeignKey(driver, on_delete = models.CASCADE)
	state = models.PositiveIntegerField(null = True, blank = True,default = 0)
	# state = 0 for scheduled ride, 1 for ongoing, 2 for completed but not rated, 3 for cancelled, 4 for rated
	otp = models.PositiveIntegerField(null = True, blank = False,)

class tempTrip(models.Model):
	LOCATION_CHOICES = (('ap', 'Airport'), ('ba', 'Baguiati'), ('lt', 'Lake Town'), ('bg', 'Beleghata'), ('rh', 'Ruby Hospital'))
	fare = models.DecimalField(decimal_places = 2, max_digits = 5, null = True, default = 0.0, blank = True)
	fromLocation = models.CharField(max_length = 150, null = True, blank = False, choices = LOCATION_CHOICES)
	toLocation = models.CharField(max_length = 150, null = True, blank = False, choices = LOCATION_CHOICES)
	riderID = models.ForeignKey(rider, on_delete = models.CASCADE)
	driverID = models.ForeignKey(driver, on_delete = models.CASCADE)


class distanceMatrix(models.Model):
	LOCATION_CHOICES = (('ap', 'Airport'), ('ba', 'Baguiati'), ('lt', 'Lake Town'), ('bg', 'Beleghata'), ('rh', 'Ruby Hospital'))
	fromLocation = models.CharField(max_length = 150, null = True, blank = False, choices = LOCATION_CHOICES)
	toLocation = models.CharField(max_length = 150, null = True, blank = False, choices = LOCATION_CHOICES)
	distance = models.DecimalField(decimal_places = 2, max_digits = 5,null = True, default = 0.0, blank = True)


class demandMatrix(models.Model):
	LOCATION_CHOICES = (('ap', 'Airport'), ('ba', 'Baguiati'), ('lt', 'Lake Town'), ('bg', 'Beleghata'), ('rh', 'Ruby Hospital'))	
	fromLocation = models.CharField(max_length = 150, null = True, blank = False, choices = LOCATION_CHOICES)
	toLocation = models.CharField(max_length = 150, null = True, blank = False, choices = LOCATION_CHOICES)
	demandValue = models.PositiveIntegerField(null = True, blank = False, default = 0)
	