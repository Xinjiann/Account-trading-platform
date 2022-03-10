from django.contrib import admin
from rango.models import Category, Page, UserProfile, GameAccount


admin.site.register(Category)
admin.site.register(Page)
admin.site.register(UserProfile)
admin.site.register(GameAccount)