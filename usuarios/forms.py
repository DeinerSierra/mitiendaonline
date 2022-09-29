from turtle import mode
from django import  forms
from .models import Cuenta, PerfilUsuario

class RegistrarForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Ingrese Password',}
    ))
    
    confirmar_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Confirmar Password',}
    ))
    
    class Meta:
        model = Cuenta
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
        
    def __init__(self, *args, **kwargs):
        super(RegistrarForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingrese nombre'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingrese apellidos'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Ingrese telefono'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese email'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            
    def clean(self):
       cleaned_data = super(RegistrarForm, self).clean()
       password = cleaned_data.get('password')
       confirmar_password = cleaned_data.get('confirmar_password')

       if password != confirmar_password:
           raise forms.ValidationError(
                "El password no coincide!"
           )
        

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            

class PerfilUsuarioForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid': ('Solo archivos de imagen')}, widget=forms.FileInput)
    class Meta:
        model = PerfilUsuario
        fields = ('direccion', 'ciudad', 'pais', 'imagen_perfil')

    def __init__(self, *args, **kwargs):
        super(PerfilUsuarioForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        