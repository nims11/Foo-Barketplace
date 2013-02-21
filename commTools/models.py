from django.db import models
from userTools.models import user_profile
from itemTools.models import items
import datetime
import logging
# Create your models here.
class Comm(models.Model):
	"""
	status codes:
		2 = Done!
		1 = Waiting!
		0 = Ongoing
		-1 = Failed (Not urgent)
	"""
	buyer = models.ForeignKey(user_profile, editable=False)
	item = models.ForeignKey(items, null=True)
	status = models.IntegerField(default=0)

class Messages(models.Model):
	time = models.DateTimeField(auto_now_add=True, editable=False)
	msg_type = models.IntegerField(default=0)
	content = models.TextField(max_length=400)
	comm = models.ForeignKey(Comm)
	user = models.ForeignKey(user_profile)

	def save(self, *args, **kwargs):
		super(Messages, self).save(*args, **kwargs)
		sender = self.user
		if sender == self.comm.buyer:
			recipient = self.comm.item.user
		else:
			recipient = self.comm.buyer

		logging.info('Messages: User id %d sent User id %d at %s for Item %s' %(sender.id, recipient.id, str(self.time), self.comm.item.title))
