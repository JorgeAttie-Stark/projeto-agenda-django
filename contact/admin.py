from django.contrib import admin

from contact import models


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'last_name', 'email', 'phone', 'created_at'
    ordering = 'id',
    list_filter = 'created_at',
    search_fields = 'id', 'first_name', 'last_name', 'email', 'phone'
    list_per_page = 1
    list_max_show_all = 100

    

# Register your models here.
