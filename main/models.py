from django.db import models
from datetime import datetime,date
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
class larderItems(models.Model):   
    
    item = models.CharField(max_length=200)
    amount = models.FloatField(null=True)
    unit = models.CharField(max_length=200)
    price = models.FloatField(null=True)
    price_unit = models.FloatField(null=True)
    user = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    
class recipes(models.Model):   

    description = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=200)
    ingredients = models.CharField(max_length=200)
    method = models.CharField(max_length=1000)
    preparation_time = models.CharField(max_length=200)
    serves = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    
class Event(models.Model):

    title = models.CharField(max_length=200)
    start_time = models.DateField()
    end_time = models.DateField()
    user = models.CharField(max_length=200)
    meal = models.CharField(max_length=200)
    