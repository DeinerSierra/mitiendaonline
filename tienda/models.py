from django.db import models
from django.urls import reverse

# Create your models here.
class Categoria(models.Model):
    categoria_nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(max_length=500, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    imagen = models.ImageField(upload_to='imagenes/productos')
    
    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
    def get_url(self):
        return reverse('categoria_productos', args=[self.slug])
    def __str__(self):
        return self.categoria_nombre
    
    
class Producto(models.Model):
    producto_nombre = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(max_length=500, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='imagenes/productos')
    cantidad = models.IntegerField()
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def get_url(self):
        return reverse('tienda:detalle_producto', args=[self.categoria.slug, self.slug])
    def __str__(self):
        return self.producto_nombre
    

class VariedadManager(models.Manager):
    def colores(self):
        super(VariedadManager, self).filter(variedad_categoria='color', is_active=True)
    def tallas(self):
        super(VariedadManager, self).filter(variedad_categoria='talla', is_active=True)
        


#Calse para los diferentes productos maneja colores y tallas etc.
variacion_categoria = [
    ('color','color'),
    ('talla','talla'),
]
class Variedad(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variedad_categoria = models.CharField(max_length=100, choices= variacion_categoria)
    variedad_valor = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    objects = VariedadManager()
    
    def __str__(self):
        return self.variedad_categoria +' : '+self.variedad_valor
    
class ProductoGaleria(models.Model):
    producto = models.ForeignKey(Producto, default=None, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='tienda/productos', max_length=255)
    
    def __str__(self):
        return self.producto.producto_nombre
