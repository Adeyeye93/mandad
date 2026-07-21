from django.db import models


class Testimonial(models.Model):
    author     = models.CharField(max_length=120)
    location   = models.CharField(max_length=120, blank=True)
    body       = models.TextField()
    rating     = models.PositiveSmallIntegerField(default=5)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author} ({self.rating}★)"


class TeamMember(models.Model):
    name         = models.CharField(max_length=120)
    role         = models.CharField(max_length=120)
    bio          = models.TextField(blank=True)
    photo        = models.ImageField(upload_to='team/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_visible   = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.name} — {self.role}"


class SiteSettings(models.Model):
    """Single-row settings table for store info."""
    phone        = models.CharField(max_length=30, default='(703) 910-6264')
    email        = models.EmailField(default='sales@mandadmedical.com')
    address      = models.TextField(default='14535 Jefferson Davis Highway, Woodbridge, VA 22191')
    hours_weekday = models.CharField(max_length=60, default='9:00 AM – 6:00 PM')
    hours_saturday = models.CharField(max_length=60, default='10:00 AM – 4:00 PM')
    hours_sunday   = models.CharField(max_length=60, default='Closed')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    def save(self, *args, **kwargs):
        # Enforce singleton
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
