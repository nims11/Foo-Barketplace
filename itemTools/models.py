from django.db import models
from userTools.models import user_profile
import logging

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
	is_expired = models.BooleanField(default=False)
	is_sold = models.BooleanField(default=False)
	buyer = models.ForeignKey(user_profile, related_name='items_buyer', blank=True, null=True)
	title_join_descrip = models.TextField(max_length=500)
	
	def __unicode__(self):
		return self.title

	def get_url(self):
		return '/item/?id=%d' % self.id

	def get_comm_url(self):
		return '/item/%d/comm/' % self.id

	class Meta:
		ordering = ['-time_create']

	def get_date(self):
		return str(self.time_create)

	def save2(self, *args, **kwargs):
		super(items, self).save(*args, **kwargs)

	def save(self, *args, **kwargs):
		self.title_join_descrip = self.title + self.descrip
		if self.id != None:
			new = False
		else:
			new = True

		super(items, self).save(*args, **kwargs)
		if new:
			logging.info('items: %s created' % self.title)
		else:
			logging.info('item: %s changed' % self.title)

	def delete(self, *args, **kwargs):
		super(items, self).delete(*args, **kwargs)
		logging.info('items: deleted %s' % self.title)
