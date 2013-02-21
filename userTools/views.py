import main
from main import handle_login_register, user
from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.api import users
from django.shortcuts import render
from forms import ProfileForm, DelForm, AddAdminForm, ConfirmForm
from models import user_profile, admins
from itemTools.models import items
from commTools.models import Comm, Messages
import logging

@handle_login_register
def user_info(request, curr_user):
	"My Profile Page"
	return render(request, 'myprofile.html', {'user_info': curr_user.get_info(), 'links': main.myprofile_links})

@handle_login_register
def edit_profile(request, curr_user):
	"Edit Profile Page"
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=curr_user.user_obj)
		if form.is_valid():
			form.save()
			return render(request, 'edit_profile.html', {'form': form, 'saved': True, 'links': main.myprofile_links})
	else:
		form = ProfileForm(instance=curr_user.user_obj)
	return render(request, 'edit_profile.html', {'form': form, 'links': main.myprofile_links})

def view_profile(request, nick):
	"Profile page of another user (nick)"
	curr_user = user(nick=nick)
	if curr_user.user_obj!=None:
		return render(request, 'view_profile.html', {'target_user': curr_user, 'user_info': curr_user.get_info(), 'links': main.user_links})
	else:
		return render(request, 'error.html', {'error': 'User %s not found!' % nick})

@handle_login_register
def del_profile(request, curr_user):
	"Delete Profile of currently logged in user"
	if request.method == 'POST':
		form = DelForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['confirm']:
				# remove all comm and messages
				comms = Comm.objects.filter(buyer=curr_user.user_obj)
				for comm in comms:
					Messages.objects.filter(comm=comm).delete()
				comms.delete()

				# remove all items
				_items = items.objects.filter(user=curr_user.user_obj)
				for item in _items:
					comms = Comm.objects.filter(item=item)
					for comm in comms:
						Messages.objects.filter(comm=comm).delete()
					comms.delete()

				# remove admin entries
				try:
					tmp = admins.objects.get(email=curr_user.user_obj.email)
					tmp.delete()
				except admins.DoesNotExist:
					pass

				# remove user
				curr_user.user_obj.delete()
				return HttpResponseRedirect(users.create_logout_url('/'))
			else:
				return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/')
	else:
		return render(request, 'user_delete.html', {'form': DelForm()})

@handle_login_register
def deact_profile(request, nick, curr_user):
	"Admin Action: Deactivate profile nick"
	# error if curr_user doesn't have the rights
	if not curr_user.is_admin:
		return render(request, 'error.html', {'error': 'You are not allowed to be here!'})
	target_user = user(nick=nick)
	# error if target user doesn't exist or is an admin
	if target_user.user_obj == None:
		return render(request, 'error.html', {'error': 'User %s does not exist!' % nick})
	if target_user.is_admin:
		return render(request, 'error.html', {'error': 'Cannot Deactivate an Admin!'})
	if not target_user.is_active:
		return render(request, 'error.html', {'error': 'User %s already deactivated!' % nick})

	if request.method == 'POST':
		form = ConfirmForm(request.POST)
		if form.is_valid():
			if not form.cleaned_data.get('confirm', False):
				return HttpResponseRedirect(target_user.user_obj.get_url())
		else:
			return HttpResponseRedirect(target_user.user_obj.get_url())
	else:
		return render(request, 'confirm.html', {'form': ConfirmForm(), 'title': 'Deactivate user %s' % nick})
	target_user.user_obj.is_active = False
	target_user.user_obj.save()
	logging.info('Admin Action: Deactivated account %s' % target_user.user_obj.nick)
	return HttpResponseRedirect(target_user.user_obj.get_url())

@handle_login_register
def act_profile(request, nick, curr_user):
	"Admin Action: Activate Profile nick"
	# error if curr_user doesn't have the rights
	if not curr_user.is_admin:
		return render(request, 'error.html', {'error': 'You are not allowed to be here!'})
	target_user = user(nick=nick)
	# error if target user doesn't exist or is an admin
	if target_user.user_obj == None:
		return render(request, 'error.html', {'error': 'User %s does not exist!' % nick})
	if target_user.is_admin:
		return render(request, 'error.html', {'error': 'Cannot Perform this operation on an Admin!'})
	if target_user.is_active:
		return render(request, 'error.html', {'error': 'User %s already activated!' % nick})

	if request.method == 'POST':
		form = ConfirmForm(request.POST)
		if form.is_valid():
			if not form.cleaned_data.get('confirm', False):
				return HttpResponseRedirect(target_user.user_obj.get_url())
		else:
			return HttpResponseRedirect(target_user.user_obj.get_url())
	else:
		return render(request, 'confirm.html', {'form': ConfirmForm(), 'title': 'Activate user %s' % nick})

	target_user.user_obj.is_active = True
	target_user.user_obj.save()
	logging.info('Admin Action: Activated account %s' % target_user.user_obj.nick)
	return HttpResponseRedirect(target_user.user_obj.get_url())

@handle_login_register
def admin_add(request, curr_user):
	"Admin Action: Add Admin"
	if not curr_user.is_admin:
		return render(request, 'error.html', {'error': 'You are not allowed to be here!'})
	if request.method == 'POST':
		form = AddAdminForm(request.POST)
		if form.is_bound and form.is_valid():
			admins(email=form.cleaned_data['email']).save()
			return render(request, 'admin_panel_add.html', {'msg': 'User with email %s given Admin rights' % form.cleaned_data['email'], 'form': AddAdminForm()})
		else:
			return render(request, 'admin_panel_add.html', {'form': form})
	else:
		return render(request, 'admin_panel_add.html', {'form': AddAdminForm()})

@handle_login_register
def admin_panel_home(request, curr_user):
	"Admin View: Admin Panel"
	if not curr_user.is_admin:
		return render(request, 'error.html', {'error': 'You are not allowed to be here!'})
	return render(request, 'admin_panel_base.html')

@handle_login_register
def deact_users(request, curr_user):
	"Admin View: Shows deactivated users"
	if not curr_user.is_admin:
		return render(request, 'error.html', {'error': 'You are not allowed to be here!'})
	ret = user_profile.objects.filter(is_active=False)
	return render(request, 'admin_panel_deact.html', {'list': ret, 'size': len(ret)})