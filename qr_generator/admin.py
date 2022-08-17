from django.contrib import admin
from .models import Category, QRCollection, UserCollection

admin.site.register(Category)
admin.site.register(QRCollection)
admin.site.register(UserCollection)
