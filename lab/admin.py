from django.contrib import admin

# Register your models here.
from lab.models import Appointment, Test

admin.site.register(Appointment)
admin.site.register(Test)
