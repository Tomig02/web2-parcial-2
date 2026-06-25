from django.contrib import messages

from django.shortcuts import redirect, render
from .forms import ContactForm

# Create your views here.
def landing_view(request):
    return render(request, 'landing/landing.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST) 
    
        if form.is_valid():
            form.save() 
            
            messages.success(request, "Mensaje enviado correctamente")
            return redirect('/contact-us') 
        else:
            messages.error(request, "Mensaje no enviado, contiene errores")    
    else:
        form = ContactForm() 
        
    return render(request, 'contact/contact.html', {'form': form})

def product_view(request):
    return render(request, 'products/products.html')

def about_us_view(request):
    return render(request, 'about_us/about_us.html')

