from django import forms
from .models import User, Facility


class Userform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phonenumber']


class Facilityform(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name']
