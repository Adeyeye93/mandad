from django.contrib import admin
from .models import Lead, NewsletterSubscriber


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display  = ['first_name', 'last_name', 'email', 'phone', 'enquiry_type', 'status', 'created_at']
    list_filter   = ['enquiry_type', 'status']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'created_at']
    list_filter  = ['is_active']
