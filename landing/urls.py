from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('contact-us', views.contact_view, name='contact'),
    path('products', views.product_view, name='products'),
    path('about-us', views.about_us_view, name='about-us'),
]