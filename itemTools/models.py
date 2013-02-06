from django.db import models
from userTools.models import user_profile

class items(models.Model):
	user = models.ForeignKey(user_profile, editable=False)
	title = models.CharField(max_length=30)
	descrip = models.TextField(max_length=400, verbose_name='Description')
	price = models.IntegerField()
	time_create = models.DateTimeField(auto_now_add=True, editable=False)
	is_active = models.BooleanField(default=True, verbose_name='Active? (Inactive items are hidden from others)')

	class Meta:
		ordering = ['-time_create']
	
	def __unicode__(self):
		return self.title

	def get_url(self):
		return '/item/?id=%d' % self.id

	def get_date(self):
		return str(self.time_create)