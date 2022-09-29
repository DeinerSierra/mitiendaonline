from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from carro.models import CarroItem
from carro.views import _cart_id

from tienda.models import Categoria, Producto

# Create your views here.
def store(request):
    productos = Producto.objects.all().filter(disponible=True)
    contexto = {'productos': productos}
    return render(request,'tienda/tienda.html', contexto)

def tienda_productos(request, categoria_slug=None):
    categorias = None
    productos = None
    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(categoria = categorias, disponible=True).order_by('id')
        paginador = Paginator(productos, 5)
        pagina = request.GET.get('pagina')
        pagina_productos = paginador.get_page(pagina)
        producto_cantidad = productos.count()
    else:
        productos = Producto.objects.all().filter(disponible=True).order_by('id')
        paginador = Paginator(productos, 5)
        pagina = request.GET.get('pagina')
        pagina_productos = paginador.get_page(pagina)
        producto_cantidad = productos.count()
        
    contexto = {'productos': pagina_productos,
                'producto_cantidad': producto_cantidad,
                }
    
    return render(request, 'tienda/productos_categorias.html', contexto)


def detalle_producto(request, categoria_slug, producto_slug):
    try:
        producto_unitario = Producto.objects.get(categoria__slug = categoria_slug, slug = producto_slug)
        en_carro = CarroItem.objects.filter(carro__carro_id = _cart_id(request), producto = producto_unitario).exists()
    except Exception as e:
        raise e
    contexto = {'producto_unitario': producto_unitario, 'en_carro': en_carro}
    
        
    return render(request,'tienda/detalle_producto.html', contexto)


def buscar_producto(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get['keyword']
        if keyword:
            productos = Producto.objects.order_by('-created_date').filter(Q(descripcion__icontains=keyword) | Q(producto_nombre__icontains=keyword))
            producto_contador = productos.count()
    contexto = {'productos': productos,
                'producto_contador': producto_contador,
                }
    return render(request,'tienda/productos_categorias.html', contexto)

    
    
