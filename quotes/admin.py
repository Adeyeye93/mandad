from django.contrib import admin
from .models import QuoteRequest, QuoteItem


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'item_type', 'quantity', 'unit_price', 'variant_info']


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display  = ['ref_number', 'first_name', 'last_name', 'email', 'phone', 'status', 'created_at']
    list_filter   = ['status', 'delivery_method']
    search_fields = ['first_name', 'last_name', 'email', 'ref_number']
    readonly_fields = ['ref_number', 'created_at', 'updated_at']
    inlines       = [QuoteItemInline]
