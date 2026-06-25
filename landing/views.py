from django.contrib import messages
from .models import UserMessages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .forms import ContactForm
from .serializers import UserMessagesSerializer, ProductoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
    # Tus datos hardcodeados en pesos
    productos_crudos = [
        {"url": "", "title": "CEPILLO DE BAMBÚ", "subtitle": "set de 2", "text": "Cepillos de dientes biodegradables con cerdas de carbón activado.", "price": "12.000"},
        {"url": "", "title": "JABÓN ARTESANAL", "subtitle": "Avena y Miel", "text": "Barra de jabón natural libre de químicos agresivos.", "price": "8.500"},
        {"url": "", "title": "COMPOSTADOR", "subtitle": "Tamaño pequeño", "text": "Pequeño compostador de cocina para residuos orgánicos.", "price": "45.000"},
        {"url": "", "title": "BOLSA DE MALLA", "subtitle": "Algodón", "text": "Bolsa reutilizable para compras a granel.", "price": "7.000"},
        {"url": "", "title": "BOMBILLAS DE BAMBÚ", "subtitle": "set de 10", "text": "Alternativa ecológica a las pajitas de plástico.", "price": "9.500"}
    ]
    
    # Pasamos los datos crudos por el serializador de DRF para que agregue el "price_usd"
    serializer = ProductoSerializer(productos_crudos, many=True)
    
    # serializer.data ahora es una lista de diccionarios limpios que ya incluyen 'price_usd'
    context = {
        'productos': serializer.data
    }
    
    # Terminamos con el return render que necesitas
    return render(request, 'products/products.html', context)

def about_us_view(request):
    return render(request, 'about_us/about_us.html')

@api_view(['GET'])
def api_datos(request):
    # 1. Traemos los objetos de la base de datos
    mensajes = UserMessages.objects.all()
    
    # 2. Los pasamos por el serializador (many=True porque es una lista de objetos)
    serializer = UserMessagesSerializer(mensajes, many=True)
    
    # 3. Retornamos la respuesta nativa de DRF
    return Response(serializer.data)

