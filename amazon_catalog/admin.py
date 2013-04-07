from django.contrib import admin
from amazon_catalog.models import *

admin.site.register(ProductGroup, admin.ModelAdmin)
admin.site.register(Product, admin.ModelAdmin)
admin.site.register(CatalogSection, admin.ModelAdmin)
