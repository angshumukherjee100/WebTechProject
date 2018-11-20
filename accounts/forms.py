from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import customUser, rider, driver, trip



class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = customUser
		fields = ('username',)


class DriverCreationForm(ModelForm):
	class Meta:
		model = driver
		fields = ['phone','name','email','license','vehicleName','vehicleNumber','carType']

class RiderCreationForm(ModelForm):
	class Meta:
		model = rider
		fields = ['phone','name','email']

class NameForm(forms.Form):
	your_name = forms.CharField(label = 'Your name', max_length = 100)
	

class TripDetailsForm(forms.Form):
	LOCATION_CHOICES = (('ap', 'Airport'), ('ba', 'Baguiati'), ('lt', 'Lake Town'), ('bg', 'Beleghata'), ('rh', 'Ruby Hospital'),)
	CAR_TYPE = (('eco','Economic'),('prem','Premium'),('suv','SUV'),)
	fromLocation = forms.ChoiceField(widget = forms.Select, choices = LOCATION_CHOICES) 
	toLocation = forms.ChoiceField(widget = forms.Select, choices = LOCATION_CHOICES)
	carType = forms.ChoiceField(widget = forms.Select, choices = CAR_TYPE)

class OTPForm(forms.Form):
	otp = forms.IntegerField(label = 'OTP', max_value = 9999, min_value = 0000)

class rateTripForm(forms.Form):
	RATING_CHOICES = ((1,1),(2,2),(3,3),(4,4),(5,5),)
	rating = forms.ChoiceField(widget = forms.Select, choices = RATING_CHOICES)