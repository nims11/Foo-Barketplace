from models import user_profile, admins
from google.appengine.api import users
from django.shortcuts import render
from forms import NickForm

myprofile_links = [('/myprofile/', 'My Profile'), ('/myprofile/edit/', 'Edit Profile'), ('/my_items/', 'My Items')]
user_links = []

class user:
	def add_user(self, obj):
		self.registered = True
		self.is_active = True
		self.user_obj = obj
		self.user_obj.save()
		try:
			admins.objects.get(email=self.user_obj.email)
			self.is_admin = True
		except admins.DoesNotExist:
			self.is_admin = False

	def get_info(self):
		ret = []
		ret.append(('Nick', self.user_obj.nick))
		if self.user_obj.f_name or self.user_obj.l_name:
			ret.append(('Name', '%s %s'%(self.user_obj.f_name, self.user_obj.l_name)))
		if self.user_obj.about_me:
			ret.append(('About Me', self.user_obj.about_me))
		if self.user_obj.email_visibility:
			ret.append(('E-mail', self.user_obj.email))
		return ret

	def __init__(self, nick=None, user_id=None, email = None):
		self.registered = False
		self.user_obj = None
		self.is_active = False
		self.is_admin = False
		if nick:
			try:
				self.user_obj = user_profile.objects.get(nick=nick)
				self.registered = True
				self.is_active = self.user_obj.is_active
				try:
					admins.objects.get(email=self.user_obj.email)
					self.is_admin = True
				except admins.DoesNotExist:
					self.is_admin = False
			except user_profile.DoesNotExist:
				self.user_obj = None
		elif user_id:
			try:
				self.user_obj = user_profile.objects.get(google_user_id=user_id)
				self.registered = True
				self.is_active = self.user_obj.is_active
				try:
					admins.objects.get(email=self.user_obj.email)
					self.is_admin = True
				except admins.DoesNotExist:
					self.is_admin = False
			except user_profile.DoesNotExist:
				self.user_obj = None
		elif email:
			try:
				self.user_obj = user_profile.objects.get(email=email)
				self.registered = True
				self.is_active = self.user_obj.is_active
				try:
					admins.objects.get(email=self.user_obj.email)
					self.is_admin = True
				except admins.DoesNotExist:
					self.is_admin = False
			except user_profile.DoesNotExist:
				self.user_obj = None

		



def handle_login_register(func):
	def handle(*args):
		user_g = users.get_current_user()
		if user_g:
			curr_user = user(email=user_g.email())
			if not curr_user.registered:
				if(args[0].method=='POST'):
					form = NickForm(args[0].POST)
					if form.is_bound and form.is_valid():
						curr_user.add_user(user_profile(google_user_id=user_g.user_id(), 
											nick=form.cleaned_data['nick'], 
											email=user_g.email()))
					else:
						return render(args[0], 'register.html', {'form': form})
				else:
					return render(args[0], 'register.html', {'form': NickForm()})
		else:
			curr_user = None
		if curr_user and not curr_user.user_obj.is_active:
			return render(args[0], 'error.html', {'error': 'You have been deactivated, contact the admin!'})
		return func(*args, curr_user=curr_user)
	return handle

def handle_optional_login(func):
	def handle(*args):
		user_g = users.get_current_user()
		if user_g:
			curr_user = user(email=user_g.email())
		else:
			curr_user = None
		return func(*args, curr_user=curr_user)
	return handle
