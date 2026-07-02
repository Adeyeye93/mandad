import json
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from products.models import Product
from .models import QuoteRequest, QuoteItem


def quote_cart(request):
    if request.method == 'POST':
        # Cart lives in localStorage — client sends it as JSON in cart_data field
        try:
            cart_items = json.loads(request.POST.get('cart_data', '[]'))
        except (json.JSONDecodeError, ValueError):
            cart_items = []

        if not cart_items:
            return render(request, 'quotes/quote_cart.html', {'error': 'Your cart is empty. Please add items before submitting.'})

        product_ids = []
        for item in cart_items:
            try:
                product_ids.append(int(item['id']))
            except (KeyError, ValueError, TypeError):
                pass
        products = {p.pk: p for p in Product.objects.filter(pk__in=product_ids)}

        qr = QuoteRequest(
            first_name      = request.POST.get('first_name', '').strip(),
            last_name       = request.POST.get('last_name', '').strip(),
            email           = request.POST.get('email', '').strip(),
            phone           = request.POST.get('phone', '').strip(),
            address         = request.POST.get('address', '').strip(),
            delivery_method = request.POST.get('delivery_method', 'delivery'),
            best_call_time  = request.POST.get('best_call_time', '').strip(),
            insurance       = '',
            notes           = request.POST.get('notes', '').strip(),
            how_heard       = request.POST.get('how_heard', '').strip(),
        )
        qr.save()

        for item in cart_items:
            try:
                p = products.get(int(item.get('id', 0)))
                if not p:
                    continue
                QuoteItem.objects.create(
                    quote        = qr,
                    product      = p,
                    product_name = item.get('name') or p.name,
                    product_sku  = getattr(p, 'sku', '') or '',
                    item_type    = item.get('type', 'purchase'),
                    quantity     = max(1, int(item.get('qty', 1))),
                    unit_price   = p.purchase_price,
                    variant_info = item.get('variant_info', ''),
                )
            except (ValueError, TypeError):
                continue

        try:
            send_mail(
                subject=f"[Mandad] New Quote Request — {qr.ref_number}",
                message=f"Ref: {qr.ref_number}\nFrom: {qr.first_name} {qr.last_name}\nEmail: {qr.email}\nPhone: {qr.phone}\nItems: {len(cart_items)}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        return render(request, 'quotes/quote_success.html', {'quote': qr})

    # GET — render empty shell; JS populates from localStorage
    return render(request, 'quotes/quote_cart.html', {})
