from django.contrib import admin

# Register your models here.
from .models import Test, Appointment, Testdata, Branch, TestTaken, Employees

admin.site.register(Appointment)
admin.site.register(Test)
admin.site.register(Testdata)
admin.site.register(Branch)
admin.site.register(TestTaken)
admin.site.register(Employees)
