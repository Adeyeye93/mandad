from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, ProductVariant, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category', 'brand', 'purchase_price', 'availability', 'is_rentable', 'is_featured', 'is_active']
    list_filter   = ['category', 'brand', 'availability', 'is_rentable', 'is_featured', 'is_active', 'is_new']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines       = [ProductImageInline, ProductVariantInline]
    fieldsets = (
        ('Core', {'fields': ('name', 'slug', 'sku', 'category', 'brand', 'short_desc', 'description')}),
        ('Pricing',  {'fields': ('purchase_price', 'compare_at_price')}),
        ('Rental',   {'fields': ('is_rentable', 'rental_weekly', 'rental_monthly', 'rental_3month')}),
        ('Inventory',{'fields': ('availability', 'stock_quantity')}),
        ('Media',    {'fields': ('main_image',)}),
        ('Specs',    {'fields': ('specs',)}),
        ('Flags',    {'fields': ('is_featured', 'is_active', 'is_new')}),
        ('SEO',      {'fields': ('meta_title', 'meta_description'), 'classes': ('collapse',)}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'display_order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['author', 'product', 'rating', 'verified', 'is_visible', 'created_at']
    list_filter   = ['rating', 'verified', 'is_visible']
    search_fields = ['author', 'product__name', 'body']
