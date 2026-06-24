from django.shortcuts import render

# Create your views here.
def landing_view(request):
    return render(request, 'landing/landing.html')

def contact_view(request):
    return render(request, 'contact/contact.html')

def product_view(request):
    return render(request, 'products/products.html')

def about_us_view(request):
    return render(request, 'about_us/about_us.html')