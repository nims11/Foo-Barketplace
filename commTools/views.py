from userTools.main import handle_login_register, user, handle_optional_login, myprofile_links
from userTools.models import user_profile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from itemTools.models import items
from forms import CommForm, DealForm, CancelForm
from models import Messages, Comm


@handle_login_register
def seller_seal(request, item_id, buyer_nick, curr_user):
	try:
		item = items.objects.get(id=item_id, is_expired=False, is_sold=False)
	except items.DoesNotExist:
		return render(request, 'error.html', {'error': 'Item Not Found'})

	try:
		tar_user = user_profile.objects.get(nick=buyer_nick)
	except user_profile.DoesNotExist:
		return render(request, 'error.html', {'error': 'User Not Found'})

	if request.method == 'POST':
		form = DealForm(request.POST)
		if form.is_valid() and form.cleaned_data.get('deal', False):
			# If sealed by buyer
			if item.user != curr_user.user_obj:
				return render(request, 'error.html', {'error': 'Not your item!'})
			else:
				# Current user is the seller
				try:
					comm = Comm.objects.get(buyer=tar_user, item=item)
				except Comm.DoesNotExist:
					return render(request, 'error.html', {'error': 'Invalid Action!!'})
				if comm.status == 1:
					item.is_sold = True
					item.buyer = tar_user
					item.save()
					comm.status = 2
					comm.save()
				else:
					return render(request, 'error.html', {'error': 'Invalid Action!!'})

	return HttpResponseRedirect(item.get_comm_url())

@handle_login_register
def cancel(request, item_id, curr_user):
	"""
	When Buyer Cancels the deal
	status = 1 -> 0
	"""
	try:
		item = items.objects.get(id=item_id, is_expired=False, is_sold=False)
	except items.DoesNotExist:
		return render(request, 'error.html', {'error': 'Item Not Found'})

	if request.method == 'POST':
		form = CancelForm(request.POST)
		if form.is_valid() and form.cleaned_data.get('cancel', False):
			if item.user != curr_user.user_obj:
				try:
					comm = Comm.objects.get(buyer=curr_user.user_obj, item=item)
				except Comm.DoesNotExist:
					return render(request, 'error.html', {'error': 'Invalid Action!!'})

				if comm.status == 1:
					comm.status = 0
					comm.save()
				else:
					return render(request, 'error.html', {'error': 'You can\'t cancel the deal now!'})
				return HttpResponseRedirect(item.get_comm_url())
			else:
				return render(request, 'error.html', {'error': 'Invalid Action!!'})
	return HttpResponseRedirect(item.get_comm_url())


@handle_login_register
def seal(request, item_id, curr_user):
	"""
	When buyer seals the deal
	status = 0 -> 1
	"""
	try:
		item = items.objects.get(id=item_id, is_expired=False, is_sold=False)
	except items.DoesNotExist:
		return render(request, 'error.html', {'error': 'Item Not Found'})

	if request.method == 'POST':
		form = DealForm(request.POST)
		if form.is_valid() and form.cleaned_data.get('deal', False):
			# If sealed by buyer
			if item.user != curr_user.user_obj:
				try:
					comm = Comm.objects.get(buyer=curr_user.user_obj, item=item)
				except Comm.DoesNotExist:
					comm = Comm(buyer=curr_user.user_obj, item=item)
					comm.save()
				if comm.status == 0:
					comm.status = 1
					comm.save()
				else:
					return render(request, 'error.html', {'error': 'You can\'t seal the deal now!'})
				return HttpResponseRedirect(item.get_comm_url())
			else:
				# Current user is the seller
				return render(request, 'error.html', {'error': 'You can\'t purchase your own item!!'})
	return HttpResponseRedirect(item.get_comm_url())


@handle_login_register
def comm_seller_buyer(request, item_id, user_nick, curr_user):
	"""
	Communication view for seller with a buyer
	"""
	try:
		item = items.objects.get(id=item_id, is_expired=False, is_sold=False)
	except items.DoesNotExist:
		try:
			item = items.objects.get(id=item_id, is_expired=False, is_sold=True)
			if item.user != curr_user.user_obj and item.buyer != curr_user.user_obj:
				return render(request, 'error.html', {'error': 'Item Not Found'})
		except items.DoesNotExist:
			return render(request, 'error.html', {'error': 'Item Not Found'})

	try:
		tar_user = user_profile.objects.get(nick=user_nick)
	except user_profile.DoesNotExist:
		return render(request, 'error.html', {'error': 'User Not Found'})

	# if the curr_user is not the seller
	if item.user != curr_user.user_obj:
		return render(request, 'error.html', {'error': 'You are not allowed to be here!'})

	try:
		comm = Comm.objects.get(buyer=tar_user, item=item)
	except Comm.DoesNotExist:
		return render(request, 'error.html', {'error': 'No communications exist!'})

	if request.method == 'POST':
		form = CommForm(request.POST)
		if form.is_valid():
			msg = form.cleaned_data['message']
			message = Messages(comm=comm, content=msg, user=curr_user.user_obj)
			message.save()
			form = CommForm()
	else:
		form = CommForm()

	# View Part
	try:
		comm = Comm.objects.get(buyer=tar_user, item=item)
		try:
			ret = Messages.objects.filter(comm=comm).order_by('-time')
		except Messages.DoesNotExist:
			ret = []
	except Comm.DoesNotExist:
		return render(request, 'error.html', {'error': 'No communications exist!'})
	return render(request, 'comm.html',{'msgs': ret, 'form': form, 'role': 'seller', 'DealForm': DealForm(), 'item': item, 'comm': comm})
	


def comm_item_seller(request, item, curr_user):
	"""
	The curr_user is the seller, show him the list of interested Buyers
	"""
	ret = Comm.objects.filter(item=item)
	return render(request, 'comm_list.html', {'comms': ret, 'item': item})

def comm_item_buyer(request, item, curr_user):
	"""
	The curr_user is the seller, show him the communication interface
	"""
	if request.method == 'POST':
		form = CommForm(request.POST)
		if form.is_valid():
			msg = form.cleaned_data['message']
			try:
				comm = Comm.objects.get(buyer=curr_user.user_obj, item=item)
			except Comm.DoesNotExist:
				comm = Comm(buyer=curr_user.user_obj, item=item)
				comm.save()
			message = Messages(comm=comm, content=msg, user=curr_user.user_obj)
			message.save()
			form = CommForm()
	else:
		form = CommForm()

	# View Part
	try:
		comm = Comm.objects.get(buyer=curr_user.user_obj, item=item)
		try:
			ret = Messages.objects.filter(comm=comm).order_by('-time')
		except Messages.DoesNotExist:
			ret = []
	except Comm.DoesNotExist:
		ret = []
		comm = Comm(buyer=curr_user.user_obj, item=item)
	return render(request, 'comm.html',{'msgs': ret, 'form': form, 'DealForm': DealForm(), 'comm': comm, 'role': 'buyer', 'item': item, 'CancelForm': CancelForm()})


@handle_login_register
def comm_item(request, item_id, curr_user):
	"""
	Returns appropriate Communication view according to seller/buyer
	"""
	try:
		item = items.objects.get(id=item_id, is_expired=False, is_sold=False)
	except items.DoesNotExist:
		try:
			item = items.objects.get(id=item_id, is_expired=False, is_sold=True)
			if item.user == curr_user.user_obj or item.buyer == curr_user.user_obj:
				pass
			else:
				return render(request, 'error.html', {'error': 'Item Not Found'})
		except items.DoesNotExist:
			return render(request, 'error.html', {'error': 'Item Not Found'})

	if curr_user.user_obj == item.user:
		return comm_item_seller(request, item, curr_user)
	else:
		return comm_item_buyer(request, item, curr_user)