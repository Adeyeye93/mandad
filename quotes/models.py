from django.db import models
from products.models import Product


class QuoteRequest(models.Model):
    """A submitted quote cart from the quote-cart page."""

    DELIVERY_CHOICES = [
        ('delivery', 'Home Delivery & Setup'),
        ('pickup',   'Pick Up In Store'),
    ]
    STATUS_CHOICES = [
        ('new',       'New'),
        ('contacted', 'Contacted'),
        ('quoted',    'Quote Sent'),
        ('won',       'Converted to Sale'),
        ('lost',      'Lost'),
    ]

    # Customer
    first_name   = models.CharField(max_length=80)
    last_name    = models.CharField(max_length=80)
    email        = models.EmailField()
    phone        = models.CharField(max_length=30)
    address      = models.TextField(blank=True)

    # Preferences
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='delivery')
    best_call_time  = models.CharField(max_length=80, blank=True)
    insurance       = models.CharField(max_length=100, blank=True)

    # Notes
    notes        = models.TextField(blank=True)
    how_heard    = models.CharField(max_length=100, blank=True)

    # Internal tracking
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    ref_number   = models.CharField(max_length=20, unique=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quote Request'
        verbose_name_plural = 'Quote Requests'

    def save(self, *args, **kwargs):
        if not self.ref_number:
            import datetime, random
            year = datetime.date.today().year
            self.ref_number = f"MMS-{year}-{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ref_number} — {self.first_name} {self.last_name} ({self.get_status_display()})"


class QuoteItem(models.Model):
    """Individual line item inside a QuoteRequest."""

    TYPE_CHOICES = [
        ('purchase', 'Purchase'),
        ('rental',   'Rental'),
    ]

    quote        = models.ForeignKey(QuoteRequest, on_delete=models.CASCADE, related_name='items')
    product      = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200, help_text="Snapshot of name at time of request")
    product_sku  = models.CharField(max_length=60, blank=True)
    item_type    = models.CharField(max_length=20, choices=TYPE_CHOICES, default='purchase')
    quantity     = models.PositiveIntegerField(default=1)
    unit_price   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    variant_info = models.CharField(max_length=300, blank=True, help_text="e.g. Colour: Camel Tan, Size: Medium")

    def __str__(self):
        return f"{self.quantity}× {self.product_name} ({self.get_item_type_display()})"

    @property
    def line_total(self):
        if self.unit_price:
            return self.unit_price * self.quantity
        return None
