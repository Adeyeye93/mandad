from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from products.models import Product, Category
from .models import RentalEnquiry


def rental_list(request):
    rentals    = Product.objects.filter(is_rentable=True, is_active=True).select_related('category', 'brand')
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        rentals = rentals.filter(category__slug=category_slug)

    ctx = {
        'rentals':        rentals,
        'categories':     categories,
        'selected_cat':   category_slug,
    }
    return render(request, 'rentals/rental_list.html', ctx)


def rental_enquiry(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product    = None
        if product_id:
            product = Product.objects.filter(pk=product_id).first()

        enquiry = RentalEnquiry(
            product         = product,
            product_name    = request.POST.get('product_name', getattr(product, 'name', '')),
            first_name      = request.POST.get('first_name', '').strip(),
            last_name       = request.POST.get('last_name', '').strip(),
            email           = request.POST.get('email', '').strip(),
            phone           = request.POST.get('phone', '').strip(),
            address         = request.POST.get('address', '').strip(),
            duration        = request.POST.get('duration', 'monthly'),
            delivery_method = request.POST.get('delivery_method', 'delivery'),
            notes           = request.POST.get('notes', '').strip(),
            how_heard       = request.POST.get('how_heard', '').strip(),
        )
        enquiry.save()

        try:
            send_mail(
                subject=f"[Mandad] New Rental Enquiry — {enquiry.product_name or 'General'}",
                message=f"From: {enquiry.first_name} {enquiry.last_name}\nEmail: {enquiry.email}\nPhone: {enquiry.phone}\nProduct: {enquiry.product_name}\nDuration: {enquiry.get_duration_display()}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, 'Rental enquiry submitted! We will contact you within 2 hours.')
        return redirect('rentals:list')

    product_id = request.GET.get('product')
    product    = None
    if product_id:
        product = Product.objects.filter(pk=product_id).first()

    return render(request, 'rentals/rental_enquiry.html', {'product': product})
