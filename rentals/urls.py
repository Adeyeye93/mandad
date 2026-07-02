from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('',        views.rental_list,    name='list'),
    path('enquiry/', views.rental_enquiry, name='enquiry'),
]
