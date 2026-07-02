from django.db import models
from products.models import Product


class RentalEnquiry(models.Model):
    """Submitted rental request from the rentals page."""

    DURATION_CHOICES = [
        ('weekly',   'Weekly'),
        ('monthly',  'Monthly'),
        ('3month',   '3+ Months'),
    ]
    DELIVERY_CHOICES = [
        ('delivery', 'Home Delivery & Setup'),
        ('pickup',   'Pick Up In Store'),
    ]
    STATUS_CHOICES = [
        ('new',        'New'),
        ('contacted',  'Contacted'),
        ('confirmed',  'Confirmed'),
        ('active',     'Active Rental'),
        ('returned',   'Returned'),
        ('cancelled',  'Cancelled'),
    ]

    # Product (optional — may be a general enquiry)
    product      = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='rental_enquiries')
    product_name = models.CharField(max_length=200, blank=True, help_text="Free-text fallback if product not in catalogue")

    # Customer
    first_name   = models.CharField(max_length=80)
    last_name    = models.CharField(max_length=80)
    email        = models.EmailField()
    phone        = models.CharField(max_length=30)
    address      = models.TextField(blank=True)

    # Rental details
    duration       = models.CharField(max_length=20, choices=DURATION_CHOICES, default='monthly')
    preferred_start = models.DateField(null=True, blank=True)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='delivery')

    # Pricing snapshot at time of enquiry
    rate_quoted  = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # Internal
    notes        = models.TextField(blank=True)
    how_heard    = models.CharField(max_length=100, blank=True)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Rental Enquiry'
        verbose_name_plural = 'Rental Enquiries'

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.product_name or (self.product.name if self.product else 'General')} ({self.get_status_display()})"
