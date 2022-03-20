from django.contrib import admin
from rango.models import Category, Page, UserProfile, GameAccount, Order


admin.site.register(Category)
admin.site.register(Page)
admin.site.register(UserProfile)
admin.site.register(GameAccount)
admin.site.register(Order)