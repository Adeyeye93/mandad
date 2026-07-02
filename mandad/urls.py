from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/',      admin.site.urls),
    path('',            include('core.urls',     namespace='core')),
    path('products/',   include('products.urls', namespace='products')),
    path('rentals/',    include('rentals.urls',  namespace='rentals')),
    path('quote-cart/', include('quotes.urls',   namespace='quotes')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
