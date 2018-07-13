from django import forms
from .import models


class CreateAppointment(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields = ['Name', 'Age', 'Date', 'Time', 'Email', 'phone_number']