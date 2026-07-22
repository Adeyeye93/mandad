from django.db import models


class Lead(models.Model):
    """General contact form submission from the Contact page."""

    ENQUIRY_TYPES = [
        ('general',   'General Enquiry'),
        ('quote',     'Product Quote'),
        ('rental',    'Rental Enquiry'),
        ('insurance', 'Insurance'),
        ('repair',    'Repair & Service'),
    ]
    STATUS_CHOICES = [
        ('new',       'New'),
        ('contacted', 'Contacted'),
        ('resolved',  'Resolved'),
    ]

    first_name    = models.CharField(max_length=80)
    last_name     = models.CharField(max_length=80)
    email         = models.EmailField()
    phone         = models.CharField(max_length=30)
    city_zip      = models.CharField(max_length=100, blank=True)
    enquiry_type  = models.CharField(max_length=20, choices=ENQUIRY_TYPES, default='general')
    product_interest = models.CharField(max_length=120, blank=True)
    best_call_time   = models.CharField(max_length=80, blank=True)
    message          = models.TextField()
    how_heard        = models.CharField(max_length=100, blank=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.get_enquiry_type_display()} ({self.created_at.date()})"


class NewsletterSubscriber(models.Model):
    email      = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active  = models.BooleanField(default=True)

    def __str__(self):
        return self.email
