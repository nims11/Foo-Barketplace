from itemTools.models import items

class foo:
	def __init__(self, boo):
		self.str = boo
		import re
		regex = re.compile('.*'+str(boo)+'.*')

	def __eq__(self, tmp):
		print tmp
		if regex.match(str(tmp)) != None:
			return False
		return True