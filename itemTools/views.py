from userTools.main import handle_login_register, user, handle_optional_login, myprofile_links
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from models import items
from forms import SellForm, DelForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from commTools.models import Comm
import datetime

expiry = datetime.timedelta(days=30)
item_per_page = 6
@handle_login_register
def sell(request, curr_user):
	"Sell Page"
	if request.method == 'POST':
		form = SellForm(request.POST, instance=items(user=curr_user.user_obj))
		if form.is_valid():
			new_item = form.save()
			# Redirect to the new item page
			return HttpResponseRedirect('/item/?id=%d' % new_item.id)
		else:
			return render(request, 'sell.html', {'form': form})
	else:
		# Display the Form
		return render(request, 'sell.html', {'form': SellForm()})

def buy(request):
	"Browse Page"
	# expiry_date = datetime.date.today()-expiry
	page_no = request.GET.get('page_no', 1)
	paginator = Paginator(items.objects.filter(is_expired=False, is_sold=False), item_per_page)
	try:
		ret = paginator.page(page_no)
	except PageNotAnInteger:
		ret = paginator.page(1)
	except EmptyPage:
		ret = paginator.page(1)

	return render(request, 'buy.html', {'items': ret, 'title': 'Buy', 'num_pages': paginator.num_pages})

@handle_optional_login
def item_view(request, curr_user):
	"Individual Item View"
	if request.method == 'GET':
		try:
			item_no = int(request.GET.get('id', -1))
		except:
			item_no = -1
	else:
		item_no = -1

	if item_no<=0:
		return render(request, 'error.html', {'error': 'Item Not Found'})
	# expiry_date = datetime.date.today()-expiry
	try:
		curr_item = items.objects.get(id=item_no)

		# if item is not expired
		if not curr_item.is_expired and not curr_item.is_sold:
			return render(request, 'item.html', {'item': curr_item})

		if curr_item.is_sold and (curr_item.user == curr_user.user_obj or curr_item.buyer == curr_user.user_obj):
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
	"Delete Item (item_id)"
	item_id = int(item_id)
	try:
		item = items.objects.get(id=item_id, is_sold=False)
	except items.DoesNotExist:
		return render(request, 'error.html', {'error': 'Item Does Not Exist or You don\'t have permission to be here!'})

	# if the curr_user has no rights
	if curr_user.user_obj != item.user and not curr_user.is_admin:
		return render(request, 'error.html', {'error': 'Item Does Not Exist or You don\'t have permission to be here!'})

	# User has rights, Perform Delete operations
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
	"Edit Item item_id"
	item_id = int(item_id)
	try:
		item = items.objects.get(id=item_id, is_sold=False)
	except items.DoesNotExist:
		return render(request, 'error.html', {'error': 'Item Does Not Exist or You don\'t have permission to be here!'})
	if curr_user.user_obj != item.user:
		return render(request, 'error.html', {'error': 'Item Does Not Exist or You don\'t have permission to be here!'})

	# User has rights, start the Edit Procedure
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
	"View for all items of a user"
	page_no = request.GET.get('page_no', 1)
	paginator = Paginator(items.objects.filter(user=curr_user.user_obj, is_sold=False), item_per_page)
	try:
		ret = paginator.page(page_no)
	except PageNotAnInteger:
		ret = paginator.page(1)
	except EmptyPage:
		ret = paginator.page(1)

	return render(request, 'my_items.html', {'items': ret, 'title': 'My Items', 'num_pages': paginator.num_pages})


@handle_login_register
def my_items_buys(request, curr_user):
	page_no = request.GET.get('page_no', 1)
	paginator = Paginator(items.objects.filter(is_sold=True, buyer=curr_user.user_obj), item_per_page)
	try:
		ret = paginator.page(page_no)
	except PageNotAnInteger:
		ret = paginator.page(1)
	except EmptyPage:
		ret = paginator.page(1)
	return render(request, 'my_items.html', {'items': ret, 'title': 'My Purchases', 'num_pages': paginator.num_pages})

@handle_login_register
def my_items_sold(request, curr_user):
	page_no = request.GET.get('page_no', 1)
	paginator = Paginator(items.objects.filter(is_sold=True, user=curr_user.user_obj), item_per_page)
	try:
		ret = paginator.page(page_no)
	except PageNotAnInteger:
		ret = paginator.page(1)
	except EmptyPage:
		ret = paginator.page(1)
	return render(request, 'my_items.html', {'items': ret, 'title': 'My Sells', 'num_pages': paginator.num_pages})

@handle_login_register
def ongoing_deals(request, curr_user):
	page_no = request.GET.get('page_no', 1)
	from itertools  import chain
	res1 = Comm.objects.filter(status=0, buyer=curr_user.user_obj)
	res2 = Comm.objects.filter(status=1, buyer=curr_user.user_obj)
	paginator = Paginator(list(chain(res1, res2)), item_per_page)
	try:
		ret = paginator.page(page_no)
	except PageNotAnInteger:
		ret = paginator.page(1)
	except EmptyPage:
		ret = paginator.page(1)
	return render(request, 'ongoing.html', {'items': ret, 'title': 'Ongoing Deals', 'num_pages': paginator.num_pages})