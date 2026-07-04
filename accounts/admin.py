from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Household, HouseholdMembership

admin.site.register(Household)
admin.site.register(HouseholdMembership)