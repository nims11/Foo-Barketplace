from itemTools.models import items
from itemTools.views import expiry
from django.http import HttpResponse
import logging
import datetime

def chk_exp(request):
	expiry_date = datetime.date.today()-expiry
	foo = items.objects.all()
	for i in foo:
		if i.is_sold == False and i.time_create.date()<expiry_date:
			i.is_expired = True
		else:
			i.is_expired = False
		i.save()
	logging.info('Cron: Expiry Check Done!')
	return HttpResponse('Done!')