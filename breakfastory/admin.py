from django.contrib import admin

from .models import MealType, Entry

# Register your models here.

admin.site.register(MealType)
admin.site.register(Entry)
