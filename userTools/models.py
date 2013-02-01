from django.db import models

class user_profile(models.Model):
	google_user_id = models.CharField(max_length=200, editable=False, unique=True)
	f_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='First Name')
	l_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='Last Name')
	nick = models.CharField(max_length=20, editable=False, unique=True)
	email_visibility = models.BooleanField(default=False, verbose_name='E-mail Visible in Profile')
	about_me = models.TextField(max_length=400, null=True, blank=True, verbose_name='About Me')
	email = models.EmailField(editable=False, unique=True)
	is_active = models.BooleanField(default=True, verbose_name='Is Active')

	def __unicode__(self):
		return self.nick

class admins(models.Model):
	email = models.EmailField(editable=False, unique=True)