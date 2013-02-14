from models import items
from dbindexer.api import register_index

register_index(items, {'title': ('icontains'), 'title_join_descrip': ('icontains')})