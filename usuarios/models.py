from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class Superusuario(BaseUserManager):
    def crear_usuario(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Email must be provided')
        if not username:
            raise ValueError('Username must be provided')
        
        usuario = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        usuario.set_password(password)
        usuario.save(using = self._db)
        return usuario
    
    def create_superuser(self, first_name, last_name, username, email, password):
        usuario = self.crear_usuario(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        usuario.is_admin = True
        usuario.is_admin = True
        usuario.is_active = True
        usuario.is_staff = True
        usuario.is_superadmin = True
        usuario.save(using=self._db)
        return usuario
 
 
 
    
class Cuenta(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=False)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name']
    
    objects = Superusuario()
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True





    
class PerfilUsuario(models.Model):
    usuario =models.OneToOneField(Cuenta, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, blank=True)
    imagen_perfil = models.ImageField(upload_to='perfilusuarios', blank=True)
    ciudad = models.CharField(max_length=25, blank=True)
    pais = models.CharField(max_length=25, blank=True)
    
    def __str__(self):
        return self.usuario.first_name

    def full_address(self):
        return f'{self.direccion}'
    
        
    
    

        
