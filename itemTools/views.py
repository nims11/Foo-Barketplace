from userTools.main import handle_login_register, user, handle_optional_login, myprofile_links
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from models import items
from forms import SellForm, DelForm
import datetime

expiry = datetime.timedelta(days=2)
@handle_login_register
def sell(request, curr_user):
	"""
	TODO: if success, redirects to that item page
	"""
	if curr_user == None:
		return render(request, 'error.html', {'error': 'Auth Failed!'})
	if request.method == 'POST':
		form = SellForm(request.POST, instance=items(user=curr_user.user_obj))
		if form.is_valid():
			form.save()
			return render(request, 'msg.html', {'msg': 'Item Posted'})
		else:
			return render(request, 'sell.html', {'form': form})
	else:
		return render(request, 'sell.html', {'form': SellForm()})

def buy(request):
	item_per_page = 10
	expiry_date = datetime.date.today()-expiry
	if request.method == 'GET':
		try:
			page_no = int(request.GET.get('page_no', 1))
		except:
			page_no = 1
	else:
		page_no = 1

	# ret is the items list to return
	# reversal of the list so that the latest creates item is at begin
	ret = items.objects.filter(time_create__gte=expiry_date)[(page_no-1)*item_per_page:(page_no-1)*item_per_page+item_per_page]
	total = len(items.objects.filter(time_create__gte=expiry_date))
	pages = total/item_per_page
	if total%item_per_page != 0:
		pages += 1
	return render(request, 'buy.html', {'items': ret, 'title': 'Buy', 
		'page_no': page_no, 
		'pages': pages,
		'pre_page': page_no-1,
		'nxt_page': page_no+1},
		)

@handle_optional_login
def item_view(request, curr_user):
	if request.method == 'GET':
		try:
			item_no = int(request.GET.get('id', -1))
		except:
			item_no = -1
	else:
		item_no = -1

	expiry_date = datetime.date.today()-expiry
	try:
		curr_item = items.objects.get(id=item_no)

		# if item is not expired
		if curr_item.time_create.date() >= expiry_date:
			return render(request, 'item.html', {'item': curr_item})

		# if the curr_user has rights to see this expired item
		if curr_user != None and (curr_item.user == curr_user.user_obj or curr_user.is_admin):
			return render(request, 'item.html', {'item': curr_item, 'expired': True})
		else:
			return render(request, 'error.html', {'error': 'Item Not Found'})
	except items.DoesNotExist:
		return render(request, 'error.html', {'error': 'Item Not Found'})

@handle_login_register
def item_delete(request, item_id, curr_user):
	if curr_user == None:
		return render(request, 'error.html', {'error': 'Auth Failed!'})
	item_id = int(item_id)
	try:
		item = items.objects.get(id=item_id)
	except items.DoesNotExist:
		return render(request, 'error.html', {'error': 'Item Does Not Exist or You don\'t have permission to be here!'})
	if curr_user.user_obj != item.user and not curr_user.is_admin:
		return render(request, 'error.html', {'error': 'Item Does Not Exist or You don\'t have permission to be here!'})

	if request.method == 'POST':
		form = DelForm(request.POST)
		if form.is_valid() and form.cleaned_data['confirm']:
			item.delete()
			return render(request, 'msg.html', {'msg': 'Item Deleted!'})
		else:
			return HttpResponseRedirect('/item/?id=%d' % item.id)
	else:
		return render(request, 'item_delete.html', {'form': DelForm(), 'item': item})

@handle_login_register
def item_edit(request, item_id, curr_user):
	if curr_user == None:
		return render(request, 'error.html', {'error': 'Auth Failed!'})
	item_id = int(item_id)
	try:
		item = items.objects.get(id=item_id)
	except items.DoesNotExist:
		return render(request, 'error.html', {'error': 'Item Does Not Exist or You don\'t have permission to be here!'})
	if curr_user.user_obj != item.user:
		return render(request, 'error.html', {'error': 'Item Does Not Exist or You don\'t have permission to be here!'})

	if request.method == 'POST':
		form = SellForm(request.POST, instance=item)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/item/?id=%d' % item.id)
		else:
			return render(request, 'edit_item.html', {'form': form, 'item': item})
	else:
		return render(request, 'edit_item.html', {'form': SellForm(instance=item), 'item': item})

@handle_login_register
def my_items(request, curr_user):
	if curr_user == None:
		return render(request, 'error.html', {'error': 'Auth Failed!'})
	item_per_page = 10
	expiry_date = datetime.date.today()-expiry
	if request.method == 'GET':
		try:
			page_no = int(request.GET.get('page_no', 1))
		except:
			page_no = 1
	else:
		page_no = 1

	# ret is the items list to return
	# reversal of the list so that the latest creates item is at begin
	ret = items.objects.filter(user=curr_user.user_obj)[(page_no-1)*item_per_page:(page_no-1)*item_per_page+item_per_page]
	total = len(items.objects.filter(user=curr_user.user_obj))
	pages = total/item_per_page
	if total%item_per_page != 0:
		pages += 1
	return render(request, 'my_items.html', {'items': ret, 'title': 'My items', 
		'page_no': page_no, 
		'pages': pages,
		'pre_page': page_no-1,
		'nxt_page': page_no+1,
		'expiry': expiry_date,
		'links': myprofile_links,
		},
		)

