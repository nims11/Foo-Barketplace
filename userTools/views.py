import main
from main import handle_login_register, user
from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.api import users
from django.shortcuts import render
from forms import ProfileForm, DelForm, AddAdminForm
from models import user_profile, admins

@handle_login_register
def user_info(request, curr_user):
	"""
	Displays the profile Page
	"""
	if curr_user != None:
		return render(request, 'myprofile.html', {'user_info': curr_user.get_info(), 'links': main.myprofile_links})
	else:
		return render(request, 'error.html', {'error': 'Auth Failed!'})

@handle_login_register
def edit_profile(request, curr_user):
	"""
	Handles the Profile Edit Page
	"""
	if curr_user == None:
		return render(request, 'error.html', {'error': 'Auth Failed!'})

	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=curr_user.user_obj)
		if form.is_valid():
			form.save()
			return render(request, 'edit_profile.html', {'form': form, 'saved': True, 'links': main.myprofile_links})
	else:
		form = ProfileForm(instance=curr_user.user_obj)
	return render(request, 'edit_profile.html', {'form': form, 'links': main.myprofile_links})

def view_profile(request, nick):
	curr_user = user(nick=nick)
	if curr_user.user_obj!=None:
		return render(request, 'view_profile.html', {'target_user': curr_user, 'user_info': curr_user.get_info(), 'links': main.user_links})
	else:
		return render(request, 'error.html', {'error': 'User %s not found!' % nick})

@handle_login_register
def del_profile(request, curr_user):
	if curr_user == None:
		return render(request, 'error.html', {'error': 'Auth Failed!'})

	if request.method == 'POST':
		form = DelForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['confirm']:
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
	# error if curr_user doesn't have the rights
	if curr_user == None or not curr_user.is_admin:
		return render(request, 'error.html', {'error': 'You are not allowed to be here!'})
	target_user = user(nick=nick)
	# error if target user doesn't exist or is an admin
	if target_user.user_obj == None:
		return render(request, 'error.html', {'error': 'User %s does not exist!' % nick})
	if target_user.is_admin:
		return render(request, 'error.html', {'error': 'Cannot Deactivate an Admin!'})
	if not target_user.is_active:
		return render(request, 'error.html', {'error': 'User %s already deactivated!' % nick})
	target_user.user_obj.is_active = False
	target_user.user_obj.save()
	return render(request, 'msg.html', {'msg': 'User %s deactivated!' % nick})

@handle_login_register
def act_profile(request, nick, curr_user):
	# error if curr_user doesn't have the rights
	if curr_user == None or not curr_user.is_admin:
		return render(request, 'error.html', {'error': 'You are not allowed to be here!'})
	target_user = user(nick=nick)
	# error if target user doesn't exist or is an admin
	if target_user.user_obj == None:
		return render(request, 'error.html', {'error': 'User %s does not exist!' % nick})
	if target_user.is_admin:
		return render(request, 'error.html', {'error': 'Cannot Perform this operation on an Admin!'})
	if target_user.is_active:
		return render(request, 'error.html', {'error': 'User %s already activated!' % nick})
	target_user.user_obj.is_active = True
	target_user.user_obj.save()
	return render(request, 'msg.html', {'msg': 'User %s Activated!' % nick})

@handle_login_register
def admin_add(request, curr_user):
	if curr_user == None or not curr_user.is_admin:
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
	if curr_user == None or not curr_user.is_admin:
		return render(request, 'error.html', {'error': 'You are not allowed to be here!'})
	return render(request, 'admin_panel_base.html')

@handle_login_register
def deact_users(request, curr_user):
	if curr_user == None or not curr_user.is_admin:
		return render(request, 'error.html', {'error': 'You are not allowed to be here!'})
	ret = user_profile.objects.filter(is_active=False)
	return render(request, 'admin_panel_deact.html', {'list': ret, 'size': len(ret)})