from django.contrib import admin
from .models import customUser,driver,rider,trip,demandMatrix,distanceMatrix,tempTrip
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(customUser)
admin.site.register(driver)
admin.site.register(rider)
admin.site.register(trip)
admin.site.register(demandMatrix)
admin.site.register(distanceMatrix)
admin.site.register(tempTrip)