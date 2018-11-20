"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView 
from django.views.generic.edit import FormView
import notifications.urls


from accounts import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('', views.home , name = 'home'),
    path('ride/',TemplateView.as_view(template_name = 'ride.html'), name = 'ride'),
    path('drive/',TemplateView.as_view(template_name = 'drive.html'), name = 'drive'),
    path('riderhome/', views.riderHome, name='riderhome'),
    path('driverhome/', views.driverHome, name='driverhome'),
    path('driversignup/', views.driverSignup.as_view() , name = 'driversignup'),
    path('ridersignup/', views.riderSignup.as_view() , name = 'ridersignup'),
    path('driverdetailsentry/', views.driverDetailsSignup.as_view() , name = 'driverdetailsform'),
    path('riderdetailsentry/', views.riderDetailsSignup.as_view() , name = 'riderdetailsform'),
    path('tripdetails/', views.TripDetails ,name = 'tripdetails'),
    path('bookride/', views.BookRide, name = 'bookride'),
    path('riderriding/', views.RiderRidingDetails, name = 'riderriding'),
    path('driverstatus/', views.driverStatus, name = 'driverstatus'),
    path('drivertripdetails/', views.driverTripDetails, name= 'drivertripdetails'),
    path('drivercancel/', views.driverCancel, name='drivercancel'),
    path('ridertripdetails/', views.riderTripDetails, name='ridertripdetails'),
    path('ridercancel/', views.riderCancel, name = 'ridercancel'),
    path('driverdriving/', views.driverDriving, name = 'driverdriving'),
    path('driverendtrip/', views.driverEndTrip, name = 'driverendtrip'),
    path('ratetrip/', views.riderTripRate, name = 'ridertriprate'),
    path('drivertriphistory/', views.driverTripHistory, name = 'drivertriphistory'),
]
