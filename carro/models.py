from django.db import models
from tienda.models import Producto, Variedad
from usuarios.models import Cuenta
# Create your models here.

class Carro(models.Model):
    carro_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.carro_id

class CarroItem(models.Model):
    usuario = models.ForeignKey(Cuenta, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variedad = models.ManyToManyField(Variedad, blank=True)
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.producto.precio * self.cantidad

    def __unicode__(self):
        return self.producto
