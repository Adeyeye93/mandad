from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Brand, Review


def product_list(request):
    qs = Product.objects.filter(is_active=True).select_related('category', 'brand')

    # Filters
    category_slug = request.GET.get('category')
    brand_slug    = request.GET.get('brand')
    availability  = request.GET.get('availability')
    min_price     = request.GET.get('min_price')
    max_price     = request.GET.get('max_price')
    sort          = request.GET.get('sort', 'featured')
    q             = request.GET.get('q', '')

    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if brand_slug:
        qs = qs.filter(brand__slug=brand_slug)
    if availability:
        qs = qs.filter(availability=availability)
    if min_price:
        qs = qs.filter(purchase_price__gte=min_price)
    if max_price:
        qs = qs.filter(purchase_price__lte=max_price)
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(description__icontains=q)

    sort_map = {
        'featured':   '-is_featured',
        'price-asc':  'purchase_price',
        'price-desc': '-purchase_price',
        'name-asc':   'name',
        'newest':     '-created_at',
    }
    qs = qs.order_by(sort_map.get(sort, '-is_featured'))

    ctx = {
        'products':       qs,
        'categories':     Category.objects.all(),
        'brands':         Brand.objects.all(),
        'selected_cat':   category_slug,
        'selected_brand': brand_slug,
        'sort':           sort,
        'q':              q,
        'total':          qs.count(),
    }
    return render(request, 'products/product_list.html', ctx)


def product_detail(request, slug):
    product   = get_object_or_404(Product, slug=slug, is_active=True)
    reviews   = product.reviews.filter(is_visible=True)
    variants  = product.variants.all()
    images    = product.images.all()
    related   = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    ctx = {
        'product':  product,
        'reviews':  reviews,
        'variants': variants,
        'images':   images,
        'related':  related,
    }
    return render(request, 'products/product_detail.html', ctx)
