from django import forms

class CommForm(forms.Form):
	"""
	 TODO: evaluate message
	"""
	message = forms.CharField(widget=forms.Textarea, max_length=400)
    
class DealForm(forms.Form):
	deal = forms.BooleanField(label='Seal The Deal?')

class CancelForm(forms.Form):
	cancel = forms.BooleanField(label='Cancel The Deal?')