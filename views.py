from django.http import HttpResponse
from django.template import Template, Context, loader, RequestContext
from django.shortcuts import render
from google.appengine.api import users
from userTools.models import user_profile, admins
from userTools.main import user
def common_proc(request):
	"""
	Provides common details
	TODO: After proper Auth Failed implementation, correct app_login_URL arguments
	"""
	user_g = users.get_current_user()
	user_reg = None
	if user_g:
		foo = user(email=user_g.email())
		if foo.user_obj == None:
			user_reg = None
		else:
			user_reg = foo
	user_nick = False
	if user_reg:
		user_nick = user_reg.user_obj.nick
	elif user_g:
		user_nick = user_g.nickname()
	return {
		'app_name': 'Foo Barketplace',
		'app_tagline': 'An open market for everyone',
		'user_nick': user_nick,
		'user_reg': user_reg,
		'user_nonreg': user_g,
		'app_login_URL': users.create_login_url(request.path),
		'app_logout_URL': users.create_logout_url(request.path),
	}

def home(request):
	return render(request, 'base.html')
