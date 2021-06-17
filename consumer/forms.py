from django import forms

# import GeeksModel from models.py
from .models import Consumer, Provider, Display, History
from django.contrib.auth.models import User


# create a ModelForm
class ConsumerForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Consumer
        fields = "__all__"
        exclude = ('user',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = "__all__"
        exclude = ('user', 'is_active')

class InfoForm(forms.ModelForm):
    class Meta:
        model = Display
        fields = "__all__"
