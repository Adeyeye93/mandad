from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name         = models.CharField(max_length=120)
    slug         = models.SlugField(unique=True, blank=True)
    description  = models.TextField(blank=True)
    icon         = models.CharField(max_length=60, blank=True, help_text="CSS class or emoji")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('in_stock',     'In Stock'),
        ('low_stock',    'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('order_only',   'Order Only'),
    ]

    # Core fields
    name         = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True, blank=True)
    category     = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand        = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', null=True, blank=True)
    sku          = models.CharField(max_length=60, unique=True, blank=True)
    description  = models.TextField(blank=True)
    short_desc   = models.CharField(max_length=300, blank=True)

    # Pricing
    purchase_price     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    compare_at_price   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original price before sale")

    # Rental
    is_rentable        = models.BooleanField(default=False)
    rental_weekly      = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rental_monthly     = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rental_3month      = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Rate per month for 3+ months")

    # Availability
    availability   = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='in_stock')
    stock_quantity = models.PositiveIntegerField(default=0)

    # Media
    main_image    = models.ImageField(upload_to='products/', blank=True, null=True)

    # Meta / SEO
    meta_title       = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=320, blank=True)

    # Flags
    is_featured  = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_new       = models.BooleanField(default=False)

    # Specs stored as JSON — flexible for different equipment types
    specs        = models.JSONField(default=dict, blank=True)

    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def on_sale(self):
        return bool(self.compare_at_price and self.purchase_price and self.compare_at_price > self.purchase_price)

    @property
    def savings(self):
        if self.on_sale:
            return self.compare_at_price - self.purchase_price
        return None

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product      = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image        = models.ImageField(upload_to='products/')
    alt_text     = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.product.name} — image {self.display_order}"


class ProductVariant(models.Model):
    """Colour, size, or model variants for a product."""
    product      = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    variant_type = models.CharField(max_length=60, help_text="e.g. Colour, Size, Model")
    value        = models.CharField(max_length=120, help_text="e.g. Camel Tan, Medium, XL")
    hex_code     = models.CharField(max_length=7, blank=True, help_text="For colour swatches e.g. #C19A6B")
    in_stock     = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} — {self.variant_type}: {self.value}"


class Review(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author     = models.CharField(max_length=120)
    location   = models.CharField(max_length=120, blank=True)
    rating     = models.PositiveSmallIntegerField(default=5)
    title      = models.CharField(max_length=200, blank=True)
    body       = models.TextField()
    verified   = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author} — {self.product.name} ({self.rating}★)"
