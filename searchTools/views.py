from userTools.main import handle_login_register, user, handle_optional_login, myprofile_links
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from itemTools.models import items
from userTools.models import user_profile
from forms import SearchItemForm, max_price
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itemTools.views import item_per_page
import datetime

def search_items(request):
	if request.method == 'GET':
		if len(request.GET) == 0:
			return render(request, 'search_form.html', {'form': SearchItemForm()})
		form = SearchItemForm(request.GET)
		if form.is_valid():
			if form.cleaned_data['search_descrip']:
				ret = items.objects.filter(is_sold=False, is_expired=False, title_join_descrip__icontains=form.cleaned_data['term']).order_by()
			else:
				ret = items.objects.filter(is_sold=False,is_expired=False, title__icontains=form.cleaned_data['term']).order_by()
			a1 = form.cleaned_data['price_from']
			a2 = form.cleaned_data['price_to']
			if a1 == -1 and a2 == -1:
				ret2 = ret
			else:
				ret2 = []
				if a2 == -1:
					a2 = max_price
				for i in ret:
					if a1 <= i.price <= a2:
						ret2.append(i)
			ret2 = ret2[::-1]
			
			page_no = request.GET.get('page_no', 1)
			paginator = Paginator(ret2, item_per_page)
			try:
				ret = paginator.page(page_no)
			except PageNotAnInteger:
				ret = paginator.page(1)
			except EmptyPage:
				ret = paginator.page(1)

			url = '?'
			for key,val in request.GET.items():
				if key != 'page_no':
					url += '%s=%s&' % (key, val)
				
			return render(request, 'search_result.html', 
				{'url': url, 'items': ret, 'title': 'Search Result for \'%s\'' % form.cleaned_data['term'], 'num_pages': paginator.num_pages})
		else:
			return render(request, 'search_form.html', {'form': form})

	else:
		return render(request, 'search_form.html', {'form': SearchItemForm()})

def search_users(request, nick):
	try:
		user = user_profile.objects.get(nick=nick)
	except user_profile.DoesNotExist:
		return render(request, 'error.html', {'error': 'User \'%s\' Not Found!' % nick})
	return HttpResponseRedirect(user.get_url())

def search_handle(request):
	if request.method == 'GET':
		if request.GET.get('field', False) == 'user':
			return search_users(request, request.GET.get('term', ''))
		elif request.GET.get('field', False) == 'item':
			return HttpResponseRedirect('/search/?term=%s&price_from=-1&price_to=-1' % request.GET.get('term',''))
	return HttpResponseRedirect('/')