from django.http import HttpResponse
from django.template import Template, Context, loader, RequestContext
from django.shortcuts import render
from google.appengine.api import users
from userTools.models import user_profile, admins
from userTools.main import user
def common_proc(request):
	"""
	Provides common details
	TODO: Handle redirection to critical pages
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
	return render(request, 'home.html')

def reset(request):
	from itemTools.models import items
	from userTools.models import user_profile, admins
	from commTools.models import Comm, Messages
	ret = ''
	for i in Messages.objects.all():
		i.delete()
	for i in Comm.objects.all():
		i.delete()
	for i in items.objects.all():
		i.delete()
	for i in user_profile.objects.all():
		i.delete()
	for i in admins.objects.all():
		i.delete()

	ret += "Previous Records Deleted!<br />"

	for i in range(1,26):
		user_profile(
			google_user_id=-1, 
			nick="test%d"%i, 
			f_name="Bob%d"%i, 
			l_name="Dylan%d"%i, 
			email="foo%d@bar.com"%i, 
			email_visibility=True, 
			about_me="abcd efgh ijkl mnop").save2()
	ret += "25 Dummy Accounts Created<br />"

	cnt = 1
	from random import randint
	for user in user_profile.objects.all():
		for i in range(10):
			items(
				user=user,
				title="item%d"%cnt,
				descrip="Awesome Item with %d blessings"%cnt,
				price=randint(1,1000000),
				).save2()
			cnt+=1

	ret += "250 Dummy Items Created<br />"
	admins(email="hardcodetest1@gmail.com").save()
	admins(email="hardcodetest2@gmail.com").save()
	ret += "\"hardcodetest2@gmail.com\" and \"hardcodetest2@gmail.com\" Given Admin Rights<br />"
	return HttpResponse(ret)