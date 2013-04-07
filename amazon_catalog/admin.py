from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from amazon_catalog.models import Category

class CategoryAdmin(MPTTModelAdmin):
    list_filter = ('level',)

admin.site.register(Category, CategoryAdmin)
