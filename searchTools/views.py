from userTools.main import handle_login_register, user, handle_optional_login, myprofile_links
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from itemTools.models import items
from userTools.models import user_profile
from forms import SearchItemForm, max_price
from itemTools.views import expiry
import datetime

def search_items(request):
	"""
	Implement pages
	Implement price range
	"""
	expiry_date = datetime.date.today()-expiry
	if request.method == 'GET':
		if len(request.GET) == 0:
			return render(request, 'search_form.html', {'form': SearchItemForm()})
		form = SearchItemForm(request.GET)
		if form.is_valid():
			if form.cleaned_data['search_descrip']:
				ret = items.objects.filter(title_join_descrip__icontains=form.cleaned_data['term']).order_by()
			else:
				ret = items.objects.filter(title__icontains=form.cleaned_data['term']).order_by()
			# if form.cleaned_data['price_from']>0:
			# 	ret = ret.filter(price__gte=form.cleaned_data['price_from']).order_by()
			# if form.cleaned_data['price_from']<max_price:
			# 	ret = ret.filter(price__lte=form.cleaned_data['price_to']).order_by()
			return render(request, 'search_result.html', {'items': ret})
		else:
			return render(request, 'search_form.html', {'form': form})

	else:
		return render(request, 'search_form.html', {'form': SearchItemForm()})

def search_users(request):
	pass