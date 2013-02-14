from django import forms
from itemTools.forms import max_price

class SearchItemForm(forms.Form):
	term = forms.CharField(min_length=3, max_length=20, label='Search Term')
	search_descrip = forms.BooleanField(label='Search in Item Description', required=False)
	price_from = forms.IntegerField(label='Min Price (-1: Skip)', min_value=-1, max_value=max_price, initial=-1)
	price_to = forms.IntegerField(label='Max Price (-1: Skip)', min_value=-1, max_value=max_price, initial=-1)


