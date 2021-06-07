from django.contrib import admin

from .models import Listing

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'address', 'is_published', 'price', 'list_date', 'realtor')

admin.site.register(Listing, ListingAdmin)
# admin.site.register(Realtor)
