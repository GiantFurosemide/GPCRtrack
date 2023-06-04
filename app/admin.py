from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import ConstructItem, ApplicationItem

admin.site.register(ConstructItem)
admin.site.register(ApplicationItem)
