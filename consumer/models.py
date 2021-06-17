from django.db import models
import datetime
from django.contrib.auth.models import User

TYPE_CHOICES = [
    ('resturant','Resturant'),
    ('individual','Individual'),
    ('organisation','organisation'),
]



# Create your models here.
class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institute_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=20)
    license = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)
    govt_agency = models.BooleanField()


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=20)
    license = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='resturant')
    institute_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

class Display(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    food_available_count = models.IntegerField()
    food_best_till = models.TimeField()

class History(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    order = models.IntegerField()
    consumer_contact_number = models.CharField(max_length=10)
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(auto_now_add=True)

