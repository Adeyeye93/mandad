from django.contrib import admin
from .models import RentalEnquiry


@admin.register(RentalEnquiry)
class RentalEnquiryAdmin(admin.ModelAdmin):
    list_display  = ['__str__', 'email', 'phone', 'duration', 'status', 'created_at']
    list_filter   = ['status', 'duration', 'delivery_method']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
