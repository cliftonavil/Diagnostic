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
    status = (
        ('Cancel', 'Canceled'),
        ('Booked', 'Booked'),
        ('Completed', 'Completed'),
        ('Ongoing', 'Ongoing'),
        ('Pendeing', 'Pending'),
    )

    app_code = models.SlugField(max_length=25, default=increment_invoice_number, unique=True, editable=True)
    app_name = models.CharField(max_length=15, name='Name')
    app_age = models.IntegerField(name='Age')
    app_date = models.DateField(name='Date')
    app_email = models.EmailField(name='Email')
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,13}$',
    #                              message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    # phone_number = models.CharField(validators=[RegexValidator(
    #     regex=r'^\+?1?\d{9,13}$',
    #     message='Username must be Alphanumeric',
    #     code='invalid_username'
    # ),],max_length=10)
    added_by = models.CharField(max_length=12,name='Addedby')


    def __str__(self):
        return self.app_code

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
    test_name = models.CharField(max_length=20, unique=True)
    test_code = models.SlugField(max_length=10, name='Code')
    referance_value = models.CharField(name='Referance', max_length=20)
    unit_value = models.CharField(name='Unit', max_length=10)
    availablity_status = models.CharField(choices=status, default='available', max_length=13 )
    test_rate = models.IntegerField(name='Rate',null=True)


    def __str__(self):
        return self.test_name


class Branch(models.Model):
    status = (
        ('active', 'Active'),
        ('shutdown', 'Shutdown'),
        ('opensoon', 'Opening Soon'),
    )
    branch_name = models.CharField(max_length=10, unique=True)
    availablity_status = models.CharField(choices=status, default='available', max_length=13 )
    branch_state = models.CharField(max_length=20, name='State')
    branch_city = models.CharField(max_length=20, name='City')
    branch_location = models.CharField(max_length=20, name='location')
    branch_address = models.TextField(name='Address')
    branch_phone_number = models.BigIntegerField(name='Phone')
    branch_email = models.EmailField(name='Email')

    def __str__(self):
        return self.branch_name

class TestTaken(models.Model):
    app_code = models.CharField(max_length=20)
    user_name = models.CharField(name='Username',max_length=20)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    result_value = models.CharField(name='ResultValue',max_length=20)
    remarks = models.CharField(name='Remarks',max_length=20)
    date = models.DateField(name='Today',default=datetime.date.today())

    def __str__(self):
        return self.app_code

class Employees(models.Model):
    # emp_code = models.CharField(max_length=5, name='Empcode')
    emp_name = models.CharField(max_length=15)
    emp_dob = models.DateField(name='DOB')
    emp_designation = models.CharField(max_length=15, name='Designation')
    emp_joiningdate = models.DateField(name='Joindate')
    emp_moobile = models.BigIntegerField(name='Mobile')
    emp_branchcode = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.emp_name


class Configuration(models.Model):
    email_use_tls = models.BooleanField(_(u'EMAIL_USE_TLS'),default=True)
    email_host = models.CharField(_(u'EMAIL_HOST'),max_length=1024)
    email_host_user = models.CharField(_(u'EMAIL_HOST_USER'),max_length=255)
    email_host_password = models.CharField(_(u'EMAIL_HOST_PASSWORD'),max_length=255)
    email_port = models.PositiveSmallIntegerField(_(u'EMAIL_PORT'),default=587)

# class EmailCongif(models.Model):
    

    # python manage.py migrate --run-syncdb
