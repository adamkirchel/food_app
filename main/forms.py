from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
import pandas as pd
from .models import larderItems, Event

unit_choices = [('kg','kg'),('ml','ml'),('L','L'),('lbs','lbs'),('g','g'),('per item','per item')]
category_choices = [('Fresh food','Fresh food'),('Pasta and grains','Pasta and grains'),('Baking items','Baking items'),('Canned items', 'Canned items'),('Drinks','Drinks'),('Snacks','Snacks'),('Other','Other')]
date_formats = ['%d-%m-%Y','%d/%m/%Y','%d/%m/%y','%d-%m-%y']
meals = [('Breakfast','Breakfast'),('Lunch','Lunch'),('Dinner','Dinner'),('Snack','Snack'),('Dessert','Dessert')]

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-input'}),label='Email:')
    password1 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class' : 'form-input'}),label='Password:')
    password2 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class' : 'form-input'}),label='Retype Password:')
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-input'}),label='Username:')
    
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
        
class LoginForm(AuthenticationForm):

    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-input'}),label='Username:')
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class' : 'form-input'}),label='Password:')
    
    class Meta:
        model = User
        fields = ("username", "password")
        
class LarderForm(forms.ModelForm):
    
    item = forms.CharField(widget=forms.TextInput(attrs={'class':'form-input'}))
    amount = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-input'}))
    unit = forms.CharField(widget=forms.Select(choices=unit_choices,attrs={'class':'form-input'}))
    price = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-input'}))
    category = forms.CharField(widget=forms.Select(choices=category_choices,attrs={'class':'form-input'}))
    
    class Meta:
        model = larderItems
        fields = ("item", "amount", "unit", "price","category")
        
        #widget = {
        #    'item': forms.TextInput(attrs={'class':'form-control'}),
         #   'amount':forms.TextInput(attrs={'class':'form-control'}),
         #   'unit':forms.Select(choices=unit_choices,attrs={'class':'form-control'}),
         #   'price':forms.TextInput(attrs={'class':'form-control'}),
         #   'category':forms.Select(choices=category_choices,attrs={'class':'form-control'}),
         #   }
         
class TimetableForm(forms.ModelForm):

    start_time = forms.DateField(input_formats=date_formats,widget=forms.TextInput(attrs={'class':'form-input'}))
    end_time = forms.DateField(input_formats=date_formats,widget=forms.TextInput(attrs={'class':'form-input'}))
    meal = forms.CharField(widget=forms.Select(choices=meals,attrs={'class':'form-input'}))
    
    class Meta:
        model = Event
        fields = ("start_time","end_time","meal")