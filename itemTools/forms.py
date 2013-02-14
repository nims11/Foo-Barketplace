from django import forms
from models import items
max_price = 1000000
class SellForm(forms.ModelForm):
    class Meta:
        model = items
        exclude = ['title_join_descrip']
    def clean_price(self):
    	price = self.cleaned_data['price']
    	if price<0:
    		raise forms.ValidationError('Non-Negative prices not allowed')
    	elif price > max_price:
    		raise forms.ValidationError('Max Price allowed is %d' % 1000000)
    	return price

class DelForm(forms.Form):
	confirm = forms.BooleanField(label='Confirm item Deletion?')