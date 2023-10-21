from django.contrib import admin
from .models import categoryList, itemList, User,itemComments, Bid
# Register your models here.
admin.site.register(User)
admin.site.register(itemList)
admin.site.register(categoryList)
admin.site.register(itemComments)
admin.site.register(Bid)