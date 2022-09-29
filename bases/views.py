from django.shortcuts import render
from tienda.models import Producto
from carro.views import _cart_id

# Create your views here.
def home(request):
    productos = Producto.objects.all().filter(disponible=True)
    contexto = {'productos': productos}
    return render(request,'bases/home.html', contexto)


