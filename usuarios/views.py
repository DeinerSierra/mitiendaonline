from django.shortcuts import render,redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .forms import RegistrarForm
from .models import Cuenta, PerfilUsuario

# Create your views here.
def registrar(request):
    form = RegistrarForm()
    if request.method == 'POST':
        form = RegistrarForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            username = email.split("@")[0]
            user = Cuenta.objects.crear_usuario(first_name=first_name, last_name=last_name, email=email, username=username, password=password )
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Se registro correctamente')
            
            
            profile = PerfilUsuario()
            profile.usuario_id = user.id
            profile.imagen_perfil = 'default/default-user.png'
            profile.save()
            
            
            current_site = get_current_site(request)
            mail_subject = 'Por favor activa tu cuenta en Ecommerce'
            body = render_to_string('usuarios/verificar_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            
            send_email.send()
            messages.success(request, 'Se ha enviado la una verificacion a correo')


            #messages.success(request, 'Se registro el usuario exitosamente')

            return redirect('/usuarios/login/?command=verification&email='+email)


    contexto = {
        'form': form
    }

    return render(request, 'usuarios/registrar.html', contexto)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('bases:home')
        else:
            messages.error(request,'Crendenciales incorrectas')
            return redirect('usuarios:login')
    return render(request, 'usuarios/login.html')



@login_required(login_url='usuarios:login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Has salido de sesion')

    return redirect('usuarios:login')

def activar(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Cuenta._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Cuenta.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Usuario activado')
        return redirect('usuarios:login')
    else:
        messages.error(request, 'Usuario no activado')
        return redirect('usuarios:registrar')
    

        
    
