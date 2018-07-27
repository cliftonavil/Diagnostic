import datetime

from django.conf import settings
from django.http import request
from django.shortcuts import render

from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Create your models here.


def increment_invoice_number():
    last_invoice = Appointment.objects.all().order_by('id').last()
    if not last_invoice:
        return 'MAG0001'
    app_code = last_invoice.app_code
    invoice_int = int(app_code.split('MAG')[-1])
    new_invoice_int = invoice_int + 1
    new_invoice_no = 'MAG' + str(new_invoice_int)
    return new_invoice_no


class Appointment(models.Model):
    app_code = models.SlugField(max_length=25, default=increment_invoice_number, unique=True, editable=True)
    app_name = models.CharField(max_length=15, name='Name')
    app_age = models.IntegerField(name='Age')
    app_date = models.DateField(name='Date')
    app_time = models.TimeField(name='Time')
    app_email = models.EmailField(name='Email')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,13}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")

    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.Name


class Testdata(models.Model):
    name = models.CharField(max_length=15)
    reporter = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Test(models.Model):
    status = (
        ('available', 'Available'),
        ('not available', 'Not Available'),
    )
    test_name = models.CharField(max_length=20, name='Name')
    test_code = models.SlugField(max_length=10, name='Code')
    referance_value = models.CharField(name='Referance', max_length=20)
    unit_value = models.CharField(name='Unit', max_length=10)
    availablity_status = models.CharField(choices=status, default='available', max_length=13, )
    test_rate = models.IntegerField(name='Rate')
    gst_tax = models.IntegerField(name='GST')

    def __str__(self):
        return self.Name


class Branch(models.Model):
    status = (
        ('active', 'Active'),
        ('shutdown', 'Shutdown'),
        ('opensoon', 'Opening Soon'),
    )
    branch_code = models.CharField(max_length=2, name='Branchcode')
    availablity_status = models.CharField(choices=status, default='available', max_length=13, )
    branch_state = models.CharField(max_length=20, name='State')
    branch_city = models.CharField(max_length=20, name='City')
    branch_location = models.CharField(max_length=20, name='location')
    branch_address = models.TextField(name='Address')
    branch_incharge = models.CharField(max_length=20, name='Incharge')
    branch_phone_number = models.IntegerField(name='Phone')
    branch_email = models.IntegerField(name='Email')

    def __str__(self):
        return self.Branchcode

    # python manage.py migrate - -run - syncdb
