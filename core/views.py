from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from products.models import Product, Category, Brand
from .models import Testimonial, TeamMember, SiteSettings
from leads.models import Lead, NewsletterSubscriber


def home(request):
    featured_products  = Product.objects.filter(is_featured=True, is_active=True)[:6]
    new_products       = Product.objects.filter(is_new=True, is_active=True)[:4]
    categories         = Category.objects.all()
    brands             = Brand.objects.all()
    testimonials       = Testimonial.objects.filter(is_visible=True)[:3]
    ctx = {
        'featured_products': featured_products,
        'new_products':      new_products,
        'categories':        categories,
        'brands':            brands,
        'testimonials':      testimonials,
    }
    return render(request, 'core/index.html', ctx)


def about(request):
    team = TeamMember.objects.filter(is_visible=True)
    ctx  = {'team': team}
    return render(request, 'core/about.html', ctx)


def contact(request):
    if request.method == 'POST':
        lead = Lead(
            first_name     = request.POST.get('first_name', '').strip(),
            last_name      = request.POST.get('last_name', '').strip(),
            email          = request.POST.get('email', '').strip(),
            phone          = request.POST.get('phone', '').strip(),
            city_zip       = request.POST.get('city_zip', '').strip(),
            enquiry_type   = request.POST.get('enquiry_type', 'general'),
            product_interest = request.POST.get('product_interest', '').strip(),
            best_call_time = request.POST.get('best_call_time', '').strip(),
            message        = request.POST.get('message', '').strip(),
            how_heard      = request.POST.get('how_heard', '').strip(),
        )
        lead.save()

        # Notify store
        try:
            send_mail(
                subject=f"[Mandad] New Contact Form — {lead.get_enquiry_type_display()}",
                message=f"From: {lead.first_name} {lead.last_name}\nEmail: {lead.email}\nPhone: {lead.phone}\n\n{lead.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, 'Thank you! We will contact you within 2 business hours.')
        return redirect('core:contact')

    site = SiteSettings.get()
    return render(request, 'core/contact.html', {'site': site})


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def accra(request):
    return render(request, 'core/accra.html', {})
