from django.contrib.auth.models import User
import django_filters

from .models import Appointment


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = ['app_code']
