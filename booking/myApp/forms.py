from django import forms
from .models import Convenience, Room, Customer
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'profile_pic', 'phonenumber']


class Roomform(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hotel', 'roomtype', 'price',
                  'capacity', 'conveniences']
