from django.contrib import admin
from apps.venues.models import Venue

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = [
        'id_display',
        'name',
        'city',
        'capacity',
        'address_display'
    ]
    search_fields = [
        'name',
        'city',
        'address'
    ]
    list_filter = [
        'city'
    ]
    readonly_fields = ['id']

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'name',
                'description',
                'address',
                'city',
                'capacity'
            )
        }),
    )

    def id_display(self, obj):
        return f"{obj.id:02d}"
    id_display.short_description = "ID"

    def address_display(self, obj):
        return obj.address or '-'
    address_display.short_description = "Адрес"
from django.contrib import admin

# Register your models here.
