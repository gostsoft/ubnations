from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Transaction, Payment_Wire, Profile, Setting

# from phone_field import PhoneField

ACCOUNT_CHOICES =(
    ("Personal", "Personal"),
        ("Merchant", "Merchant"),
)

class Reg_user(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=10, min_length=10, label="Phone")    
    ssn = forms.CharField(max_length=50, label="S S N")
    account_type = forms.ChoiceField(choices = ACCOUNT_CHOICES,label="Acccount")
    

    class Meta:
        model= User
        fields = ["first_name", "last_name", "username", "phone", "email", "ssn","password1", "password2","account_type" ]
        # fields = '__all__'

"""Dp form"""
class Dp(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]

"""Profile info form"""
class Prof(forms.ModelForm):
    city = forms.CharField(max_length=50, label="City")
    state = forms.CharField(max_length=50, label="State")
    country = forms.CharField(max_length=50, label="Country")
    address = forms.CharField(max_length=50, label='Address')
    dob = forms.DateField( label="D O B")



    class Meta:
        model = Setting
        fields = ['address', 'city', 'state', 'country', 'dob', 'id_card']

"""Settings form"""
class Set(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

"""Payment form"""

class Payment_form(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['user', 'date', 'progress', 'type_of', 'swift_code']


class Wire_Payment_form(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['user', 'date', 'progress', 'type_of']