from django.db import models
import logging

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

	def get_url(self):
		return '/user/%s/' % self.nick

	def save2(self, *args, **kwargs):
		super(user_profile, self).save(*args, **kwargs)

	def save(self, *args, **kwargs):
		if user_profile.objects.filter(nick=self.nick).exists():
			new = False
		else:
			new = True

		super(user_profile, self).save(*args, **kwargs)
		if new:
			logging.info('user_profile: %s created' % self.nick)
		else:
			logging.info('user_profile: %s changed' % self.nick)

	def delete(self, *args, **kwargs):
		super(user_profile, self).delete(*args, **kwargs)
		logging.info('user_profile: deleted %s' % self.nick)



class admins(models.Model):
	email = models.EmailField(editable=False, unique=True)

	def save(self, *args, **kwargs):
		super(admins, self).save(*args, **kwargs)
		logging.info('admins: added %s' % self.email)

	def delete(self, *args, **kwargs):
		super(admins, self).delete(*args, **kwargs)
		logging.info('admins: deleted %s' % self.email)