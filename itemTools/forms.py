from django.forms import ModelForm, Form
from django import forms
from models import items

class SellForm(ModelForm):
    class Meta:
        model = items

class DelForm(forms.Form):
	confirm = forms.BooleanField(label='Confirm item Deletion?')