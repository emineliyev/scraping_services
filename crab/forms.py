from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                  to_field_name='slug', required=False, label='Şəhər')
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      to_field_name='slug', required=False, label='Kateqoriya')




