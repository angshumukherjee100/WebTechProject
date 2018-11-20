from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, CreateView, FormView
from .models import customUser,driver,rider,trip,demandMatrix,distanceMatrix, tempTrip
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CustomUserCreationForm, DriverCreationForm, RiderCreationForm, TripDetailsForm, OTPForm, rateTripForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate, logout
import math
from django.contrib.sessions.models import Session
from django.utils import timezone
import random
from notifications.signals import notify

def home(request):
    if request.user.is_authenticated:
        currentUser = request.user
        allDrivers = driver.objects.all()
        for registeredDriver in allDrivers:
            if registeredDriver.user == currentUser:
                return HttpResponseRedirect(reverse_lazy('driverhome'))
        allRiders = rider.objects.all()
        for registeredRider in allRiders:
            if registeredRider.user == currentUser:
                return HttpResponseRedirect(reverse_lazy('riderhome'))
    else:
        return render(request, 'home.html')

def riderHome(request):
	#Add check whether logged in user is really a rider or not
	return render(request,'riderhome.html')

def driverHome(request):
	#Add check whether logged in user is really a driver or not
	return render(request,'driverhome.html')

class driverSignup(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('driverdetailsform')
    template_name = 'signup.html'

    def form_valid(self, form):
    	self.object = form.save()
    	my_driver = driver(user = self.object)
    	my_driver.save()
    	login(self.request, customUser.objects.get(username = self.request.POST['username']))
    	return HttpResponseRedirect(self.get_success_url())

class riderSignup(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('riderdetailsform')
    template_name = 'signup.html'

    def form_valid(self, form):
    	self.object = form.save()
    	my_rider = rider(user = self.object)
    	my_rider.save()
    	login(self.request, customUser.objects.get(username = self.request.POST['username']))
    	return HttpResponseRedirect(self.get_success_url())

class driverDetailsSignup(UpdateView):
    form_class = DriverCreationForm
    success_url = reverse_lazy('driverhome')
    template_name = 'driverdetailsform.html'

    def get_object(self):
    	user_object = customUser.objects.get(username = self.request.user.username)
    	return driver.objects.get(user = user_object)


class riderDetailsSignup(UpdateView):
    form_class = RiderCreationForm
    success_url = reverse_lazy('riderhome')
    template_name = 'riderdetailsform.html'

    def get_object(self):
    	user_object = customUser.objects.get(username = self.request.user.username)
    	return rider.objects.get(user = user_object)


def TripDetails(request):
    if request.method == 'POST':
        form = TripDetailsForm(request.POST)
        if form.is_valid():
            fL = form.cleaned_data['fromLocation']
            tL = form.cleaned_data['toLocation']
            cg = form.cleaned_data['carType']
            if fL == tL:
                return render(request, 'tripdetails.html', {'form': form})
            baseFareObject = distanceMatrix.objects.get(fromLocation = fL, toLocation = tL)
            flexiFareObject = demandMatrix.objects.get(fromLocation = fL, toLocation = tL)
            if cg == 'eco':
                fare = float(baseFareObject.distance)*7 
            elif cg == 'prem':
                fare = float(baseFareObject.distance)*9
            else:
                fare = float(baseFareObject.distance)*10
            
            fare += (5/(1 + math.exp(-1*(float(flexiFareObject.demandValue) - 5)))) * 25
            fare = int(fare)
            


            request.session['fromLocation'] = fL
            request.session['toLocation'] = tL
            request.session['fare'] = fare
            request.session['carType'] = cg

            return HttpResponseRedirect(reverse_lazy('bookride'))
    else:
        form = TripDetailsForm()
    
    return render(request, 'tripdetails.html', {'form': form})

def BookRide(request):
    fL = request.session['fromLocation']
    tL = request.session['toLocation']
    fare = request.session['fare']
    fromLocation = [item for item in distanceMatrix.LOCATION_CHOICES if item[0] == fL][0][1] 
    toLocation = [item for item in distanceMatrix.LOCATION_CHOICES if item[0] == tL][0][1]
    flexiFareObject = demandMatrix.objects.get(fromLocation = fL, toLocation = tL)
    return render(request, 'booktrip.html', { 'toLocation' : toLocation , 'fromLocation' : fromLocation, 'fare' : fare })

def RiderRidingDetails(request):
    fL = request.session['fromLocation']
    tL = request.session['toLocation']
    fare = request.session['fare']
    category = request.session['carType']
    fromLocation = [item for item in distanceMatrix.LOCATION_CHOICES if item[0] == fL][0][1] 
    toLocation = [item for item in distanceMatrix.LOCATION_CHOICES if item[0] == tL][0][1]
    flexiFareObject = demandMatrix.objects.get(fromLocation = fL, toLocation = tL)
    flexiFareObject.demandValue += 1.0
    flexiFareObject.save()
    querySet = get_current_users()
    driverQuerySet = driver.objects.all()
    activeDrivers = []
    for activeUser in querySet:
        for registeredDrivers in driverQuerySet:
            if registeredDrivers.user == activeUser:
                activeDrivers.append(registeredDrivers)
    activeDriversOfRequestedCategory = []
    for activeDriver in activeDrivers:
        if activeDriver.state == 0 and activeDriver.carType == category and activeDriver.lastLocation == fL:	#Check last location here.
            activeDriversOfRequestedCategory.append(activeDriver)
    if len(activeDriversOfRequestedCategory) == 0:
        return render(request, 'riderridingdetails.html', {'isDriverAvailable' : 0 })
    else:
        chosenDriver = activeDriversOfRequestedCategory[0]
        ridersQuerySet = rider.objects.all()
        currRider = None
        for registeredRider in ridersQuerySet:
            if registeredRider.user == request.user:
                currRider = registeredRider
        temporaryTrip = tempTrip(fare = fare, fromLocation = fL, toLocation = tL, riderID = currRider , driverID = chosenDriver)
        temporaryTrip.save()
        notify.send(request.user, recipient=chosenDriver.user, verb=' has sent you a ride request on ')
        chosenDriver.state = 1
        chosenDriver.save()	
        return render(request, 'riderridingdetails.html', {'isDriverAvailable' : 1})


def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return customUser.objects.filter(id__in=user_id_list)

def driverStatus(request):
    currDriver = None
    registeredDrivers = driver.objects.all()
    for registeredDriver in registeredDrivers:
        if registeredDriver.user == request.user:
            currDriver = registeredDriver
    if currDriver.state == 0:
        return render(request, 'driverstatus.html', {'state' : 0})
    elif currDriver.state == 1:
        return render(request, 'driverstatus.html', {'state' : 1})
    else:
        return render(request, 'driverstatus.html', {'state' : 2})

def driverTripDetails(request):			#driver's view function when he accepts the ride
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            OTP = form.cleaned_data['otp']
            currDriver = None
            registeredDrivers = driver.objects.all()
            for registeredDriver in registeredDrivers:
                if registeredDriver.user == request.user:
                    currDriver = registeredDriver			
            tripObject = trip.objects.get(driverID = currDriver, state = 0)
            if OTP == tripObject.otp:
                tripObject.state = 1
                tripObject.save()
                return render(request, 'driverdriving.html', {})
            else:
                otpMessage = "Incorrect OTP"
                return render(request, 'drivertripdetails.html', {'tripObject' : tripObject, 'form' : form, 'message' : otpMessage})
			
	
    else:
        currDriver = None
        registeredDrivers = driver.objects.all()
        for registeredDriver in registeredDrivers:
            if registeredDriver.user == request.user:
                currDriver = registeredDriver

        tempTripQueryList = tempTrip.objects.all()
        requiredtempTripObject = None
        for tempTripObject in tempTripQueryList:
            if tempTripObject.driverID == currDriver:
                requiredtempTripObject = tempTripObject

        tempTripObject = requiredtempTripObject
		
        currRider = rider.objects.get(user = tempTripObject.riderID.user)
        currRider.state = 1
        currRider.save()

        currDriver.state = 2
        currDriver.save()

        OTP = random.randint(1000,9999)
        tripObject = trip(fare = tempTripObject.fare, fromLocation = tempTripObject.fromLocation, toLocation = tempTripObject.toLocation, riderID = tempTripObject.riderID, driverID = tempTripObject.driverID, startTime = timezone.now(), state = 0, otp = OTP)
        tripObject.save()
        notify.send(request.user, recipient=currRider.user, verb=' has accepted your ride on ')
        requiredtempTripObject.delete()

        form = OTPForm()
        otpMessage = ""
        return render(request, 'drivertripdetails.html', {'tripObject' : tripObject, 'form' : form , 'message' : otpMessage})


def driverCancel(request):
    currDriver = None
    registeredDrivers = driver.objects.all()
    for registeredDriver in registeredDrivers:
        if registeredDriver.user == request.user:
            currDriver = registeredDriver
    
    tempTripQueryList = tempTrip.objects.all()
    requiredtempTripObject = None
    for tempTripObject in tempTripQueryList:
        if tempTripObject.driverID == currDriver:
            requiredtempTripObject = tempTripObject
    category = currDriver.carType

    querySet = get_current_users()
    driverQuerySet = driver.objects.all()
    activeDrivers = []
    for activeUser in querySet:
        for registeredDrivers in driverQuerySet:
            if registeredDrivers.user == activeUser:
                activeDrivers.append(registeredDrivers)
    activeDriversOfRequestedCategory = []
    for activeDriver in activeDrivers:
        if activeDriver.state == 0 and activeDriver.carType == category and activeDriver.lastLocation == tempTripObject.fromLocation:
            activeDriversOfRequestedCategory.append(activeDriver)
    if len(activeDriversOfRequestedCategory) == 0:
        flexiFareObject = demandMatrix.objects.get(fromLocation = requiredtempTripObject.fromLocation, toLocation = requiredtempTripObject.toLocation)
        flexiFareObject.demandValue -= 1.0
        flexiFareObject.save()
        requiredtempTripObject.delete()
    else:
        random.shuffle(activeDriversOfRequestedCategory)
        chosenDriver = activeDriversOfRequestedCategory[0]
        tempTripQueryList.driverID = chosenDriver
        chosenDriver.state = 1
        chosenDriver.save()	
    
    currDriver.state = 0
    currDriver.save()


    return HttpResponseRedirect(reverse_lazy('driverhome'))

def driverTripHistory(request):
    currDriver = None
    driverTripList = []
    registeredDrivers = driver.objects.all()
    for registeredDriver in registeredDrivers:
        if registeredDriver.user == request.user:
            currDriver = registeredDriver

    tripQueryList = trip.objects.all()
    for tripObject in tripQueryList:
        if tripObject.driverID == currDriver:
            driverTripList.append(tripObject)
    driverTripList.reverse()
    rateList = [1,2,3,4,5]
    return render(request,'drivertriphistory.html', {"driverTripList":driverTripList, "currDriver": currDriver, "rateList" : rateList})        

def riderTripDetails(request):
    currRider = None
    riderTriplist = []
    registeredRiders = rider.objects.all()
    for registeredRider in registeredRiders:
        if registeredRider.user == request.user:
            currRider = registeredRider

    tripQueryList = trip.objects.all()
    for tripObject in tripQueryList:
        if  tripObject.riderID == currRider:
            riderTriplist.append(tripObject)
    riderTriplist.reverse()
    rateList=[1,2,3,4,5]
    return render(request,'ridertripdetails.html', {"riderTriplist" : riderTriplist, "currRider": currRider, "rateList" : rateList})


def riderCancel(request):
    fL = request.session['fromLocation']
    tL = request.session['toLocation']
    currRider = None
    riderTriplist = []
    registeredRiders = rider.objects.all()
    for registeredRider in registeredRiders:
        if registeredRider.user == request.user:
            currRider = registeredRider

    tripObject = trip.objects.get(riderID = currRider, state = 0)
    driverObject = tripObject.driverID
    driverObject.state = 0
    driverObject.save()
    currRider.state = 0
    currRider.save()
    tripObject.state = 3
    tripObject.save()
    flexiFareObject = demandMatrix.objects.get(fromLocation = fL, toLocation = tL)
    flexiFareObject.demandValue -= 1.0
    flexiFareObject.save()

    return HttpResponseRedirect(reverse_lazy('ridertripdetails'))


def driverDriving(request):
	render(request, 'driverdriving.html', {})

def driverEndTrip(request):
    currDriver = None
    registeredDrivers = driver.objects.all()
    for registeredDriver in registeredDrivers:
        if registeredDriver.user == request.user:
            currDriver = registeredDriver
    tripObject = trip.objects.get(driverID = currDriver, state = 1)
    currRider = tripObject.riderID
    tripObject.endTime = timezone.now()
    tripObject.state = 2
    tripObject.save()
    currDriver.state = 0
    currDriver.numberOfTrips += 1
    currDriver.lastLocation = tripObject.toLocation
    currDriver.save()
    currRider.state = 0
    currRider.save()
    flexiFareObject = demandMatrix.objects.get(fromLocation = tripObject.fromLocation, toLocation = tripObject.toLocation)
    flexiFareObject.demandValue -= 1.0
    flexiFareObject.save()

    return HttpResponseRedirect(reverse_lazy('driverhome'))

def riderTripRate(request):
	if request.method == 'POST':
		form = rateTripForm(request.POST)
		if form.is_valid():
			rating = form.cleaned_data['rating']
			currRider = None
			registeredRiders = rider.objects.all()
			for registeredRider in registeredRiders:
				if registeredRider.user == request.user:
					currRider = registeredRider

			tripObject = trip.objects.get(riderID = currRider, state = 2)
			tripObject.state = 4
			

			driverObject = driver.objects.get(user = tripObject.driverID.user)
			driverObject.rating = int(float(driverObject.rating) * (int(driverObject.numberOfTrips) - 1)  + int(rating))/int(driverObject.numberOfTrips)
			driverObject.save()
			tripObject.save()

			return HttpResponseRedirect(reverse_lazy('riderhome'))
	else:
		form = rateTripForm()
    
	return render(request, 'riderratetrip.html', {'form': form})