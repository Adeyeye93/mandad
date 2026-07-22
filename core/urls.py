from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',            views.home,                 name='home'),
    path('about/',      views.about,                name='about'),
    path('financing/',  views.financing,            name='financing'),
    path('contact/',    views.contact,              name='contact'),
    path('newsletter/', views.newsletter_subscribe, name='newsletter'),
    path('accra/',      views.accra,                name='accra'),
]
