from django.db import models
from userTools.models import user_profile


class items(models.Model):
	"""
	is_active yet to be implemented into the App
	"""
	user = models.ForeignKey(user_profile, editable=False)
	title = models.CharField(max_length=30)
	descrip = models.TextField(max_length=400, verbose_name='Description')
	price = models.IntegerField()
	time_create = models.DateTimeField(auto_now_add=True, editable=False)
	is_active = models.BooleanField(default=True, verbose_name='Active? (Inactive items are hidden from others)')
	title_join_descrip = models.TextField(max_length=500)
	
	def __unicode__(self):
		return self.title

	def get_url(self):
		return '/item/?id=%d' % self.id

	class Meta:
		ordering = ['-time_create']

	def get_date(self):
		return str(self.time_create)

	def save(self, *args, **kwargs):
		self.title_join_descrip = self.title + self.descrip
		super(items, self).save(*args, **kwargs)