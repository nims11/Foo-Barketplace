from itemTools.models import items
from itemTools.views import expiry
from django.http import HttpResponse
import logging
import datetime

def chk_exp(request):
	expiry_date = datetime.date.today()-expiry
	items.objects.filter(time_create__lt=expiry_date, is_expired=False).update(is_expired=True)
	logging.info('Cron: Expiry Check Done!')
	return HttpResponse('Done!')