from django.contrib import admin
from .models import Site, Page, Shortcode
# Register your models here.

admin.site.register(Site)
admin.site.register(Page)
admin.site.register(Shortcode)
