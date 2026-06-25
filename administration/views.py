from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from . import forms
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import AuthorizedUsers, CustomUser
from collections import Counter
from landing.models import UserMessages 
from django.core.mail import send_mail
from django.conf import settings

@user_passes_test(lambda u: u.is_authenticated, login_url='/admin/login')
def my_custom_admin_view(request):
    messages = list(UserMessages.objects.all().order_by("-id"))

    for msg in messages:
        msg.category = classify_message(msg.message)

    total = len(messages)
    counts = Counter(msg.category for msg in messages)

    context = {
        "data": messages,
        "total": total,
        "counts": counts,
    }

    return render(request, "administration/system.html", context)

def recovery_view(request):
    form = forms.RecoveryForm()
    context = {'form': form, 'page_action': "Verificacion"} 
    return render(request, 'administration/form-panel.html', context)

def register_view(request):
    if 'submit_verification' in request.POST:
        user_code = request.POST.get('verification_code')
        saved_code = request.session.get('email_verification_code')
        
        if user_code == saved_code:
            form_data = request.session.get('pending_form_data')
            form = forms.RegisterForm(form_data)
            if form.is_valid():
                form.save()
                del request.session['pending_form_data']
                del request.session['email_verification_code']

                messages.success(request, "Usuario creado correctamente")
                return redirect('/admin/login')
        else:
            # Code failed. Reload form from session to show it again
            form_data = request.session.get('pending_form_data')
            form = forms.RegisterForm(form_data)
            return render(request, 'administration/form-panel.html', {
                'form': form, 
                'show_verification': True,
                'verification_error': 'Invalid code. Please try again.'
            })
    elif request.method == 'POST':
        form = forms.RegisterForm(request.POST) 

        print(form.is_valid())
        print(form.error_messages)
        if True: #form.is_valid()
            email_a_buscar = form.cleaned_data["username"]
            print("POST:", request.POST)
            print("CLEANED:", form.cleaned_data)
            print(email_a_buscar)
            aprobado = AuthorizedUsers.objects.filter(email=email_a_buscar).exists()
            ya_existe = CustomUser.objects.filter(email=email_a_buscar).exists()

            print(ya_existe)
            print(aprobado)
            if aprobado and not ya_existe:
                request.session['pending_form_data'] = request.POST.dict()
                usuario = AuthorizedUsers.objects.get(email=email_a_buscar)
                request.session['email_verification_code'] = usuario.code
                send_email_verification(usuario.email, usuario.code)

                return render(request, 'administration/form-panel.html', {'form': form, 'show_verification': True})
        messages.error(request, "La informacion contiene errores, ingrese nuevamente")
    else:
        form = forms.RegisterForm()

    context = {'form': form, 'page_action': "Verificacion"} 
    return render(request, 'administration/form-panel.html', context)

class CustomLoginView(LoginView):
    template_name = 'administration/form-panel.html'
    form_class = forms.CustomLoginForm 
    redirect_authenticated_user = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_action'] = 'Login' 
        return context

    def get_success_url(self):
        return reverse_lazy('administration:custom_admin_dashboard')
    

def send_email_verification(email, code):
    print("enviando codigo" + code)
    subject = "Código de verificación"
    message = f"Tu código de verificación es: {code}"

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


from django.shortcuts import get_object_or_404, redirect

def delete_message(request, pk):
    if request.method == "POST":
        message = get_object_or_404(UserMessages, pk=pk)
        message.delete()

    return redirect("/admin/")


from .forms import UserMessageForm

def edit_message(request, pk):
    message = get_object_or_404(UserMessages, pk=pk)

    if request.method == "POST":
        message.name = request.POST.get("name")
        message.surname = request.POST.get("surname")
        message.email = request.POST.get("email")
        message.phone = request.POST.get("phone")
        message.message = request.POST.get("message")
        message.save()

    return redirect("/admin/")

def classify_message(text: str) -> str:
    text = text.lower()

    if any(word in text for word in ["precio", "costo", "tarifa", "compra"]):
        return "Consulta_Comercial"

    elif any(word in text for word in ["soporte", "error", "problema", "ayuda"]):
        return "Consulta_Técnica"

    elif any(word in text for word in ["trabajo", "cv", "empleo", "linkedin"]):
        return "Consulta_de_RRHH"

    return "Consulta_General"