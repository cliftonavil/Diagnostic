import datetime

from django.db import models
# Create your models here.

def increment_code():
    last_app_code = Appointment.objects.all().order_by('id').last()
    if not last_app_code:
        return 'RNH' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '0000'
        app_code = last_app_code.app_code
    booking_int = int(app_code[9:13])
    new_booking_int = booking_int + 1
    new_booking_id = 'RNH' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(
        new_booking_int).zfill(4)
    return new_booking_id


class Appointment(models.Model):
    app_code = models.SlugField(max_length=25, default=increment_code, unique=True, editable=True)
    app_name = models.CharField(max_length=15, name='Name')
    app_age = models.IntegerField(name='Age')
    app_date = models.DateField(name='Date')
    app_time = models.TimeField(name='Time')

    #
    # def __str__(self):
    #     return self.Name


class Test(models.Model):
    status = (
        ('available', 'Available'),
        ('not available', 'Not Available'),
    )
    test_name = models.CharField(max_length=20, name='Name')
    test_code = models.CharField(max_length=10, name='Code')
    referance_value = models.CharField(name='Referance', max_length=20)
    unit_value = models.CharField(name='Unit',max_length=10)
    availablity_status = models.CharField(choices=status, default='available', max_length=13,)
    test_rate = models.IntegerField(name='Rate')
    gst_tax = models.IntegerField(name='GST')

    # def __str__(self):
    #     return self.Name