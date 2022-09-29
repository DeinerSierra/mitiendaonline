from django.shortcuts import render, redirect, get_object_or_404
from tienda.models import Producto, Variedad
from .models import Carro, CarroItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Producto.objects.get(id=product_id)

    current_user = request.user

    if current_user.is_authenticated:
        #aqui en este bloque agregaremos la logica del carrito de compras cuando
        #el usuario esta autenticado
        product_variation = []

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variedad.objects.get(producto=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass



        is_cart_item_exists = CarroItem.objects.filter(producto=product, usuario=current_user).exists()

        if is_cart_item_exists:
            cart_item = CarroItem.objects.filter(producto=product, usuario=current_user)

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variedad.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation  in ex_var_list:
                  index = ex_var_list.index(product_variation)
                  item_id = id[index]
                  item = CarroItem.objects.get(producto=product, id=item_id)
                  item.cantidad += 1
                  item.save()
            else:
                item = CarroItem.objects.create(producto=product, cantidad=1, user=current_user)
                if len(product_variation) > 0 :
                    item.variedad.clear()
                    item.variedad.add(*product_variation)
                item.save()

        else:
            cart_item = CarroItem.objects.create(
                producto = product,
                cantidad = 1,
                usuario = current_user ,
            )
            if len(product_variation) > 0 :
                cart_item.variedad.clear()
                cart_item.variedad.add(*product_variation)
            cart_item.save()

        return redirect('carrito:carro')

    else:
        product_variation = []

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variedad.objects.get(producto=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        try:
            cart = Carro.objects.get(carro_id=_cart_id(request))
        except Carro.DoesNotExist:
            cart = Carro.objects.create(
                
                carro_id = _cart_id(request)
            )
        cart.save()



        is_cart_item_exists = CarroItem.objects.filter(producto=product, carro=cart).exists()
        if is_cart_item_exists:
            cart_item = CarroItem.objects.filter(producto=product, carro=cart)

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variedad.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation  in ex_var_list:
                  index = ex_var_list.index(product_variation)
                  item_id = id[index]
                  item = CarroItem.objects.get(producto=product, id=item_id)
                  item.cantidad += 1
                  item.save()
            else:
                item = CarroItem.objects.create(producto=product, cantidad=1, carro=cart)
                if len(product_variation) > 0 :
                    item.variedad.clear()
                    item.variedad.add(*product_variation)
                item.save()

        else:
            cart_item = CarroItem.objects.create(
                producto = product,
                cantidad = 1,
                carro = cart,
            )
            if len(product_variation) > 0 :
                cart_item.variedad.clear()
                cart_item.variedad.add(*product_variation)
            cart_item.save()

        return redirect('carrito:carro')


def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Producto, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CarroItem.objects.get(producto=product, usuario=request.user, id=cart_item_id)
        else:
            cart = Carro.objects.get(carro_id=_cart_id(request))
            cart_item = CarroItem.objects.get(producto=product, carro=cart, id=cart_item_id)
        if cart_item.cantidad > 1:
            cart_item.cantidad -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('carrito:carro')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Producto, id=product_id)

    if request.user.is_authenticated:
        cart_item = CarroItem.objects.get(producto=product, usuario=request.user, id=cart_item_id)
    else:
        cart = Carro.objects.get(carro_id=_cart_id(request))
        cart_item = CarroItem.objects.get(producto=product, carro=cart, id=cart_item_id)

    cart_item.delete()
    return redirect('carrito:carro')


def carro(request, total=0, cantidad=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CarroItem.objects.filter(usuario=request.user, is_active=True)
        else:
            cart = Carro.objects.get(carro_id=_cart_id(request))
            cart_items = CarroItem.objects.filter(carro=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.producto.precio * cart_item.cantidad)
            cantidad += cart_item.cantidad
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass ## solo ignora la exception

    context = {
        'total': total,
        'cantidad': cantidad,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total': grand_total
    }

    return render(request, 'carro/carro.html', context)


@login_required(login_url='usuarios:login')
def checkout(request, total=0, cantidad=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:

        if request.user.is_authenticated:
            cart_items = CarroItem.objects.filter(usuario=request.user, is_active=True)
        else:
            cart = Carro.objects.get(carro_id=_cart_id(request))
            cart_items = CarroItem.objects.filter(carro=cart, is_active=True)



        for cart_item in cart_items:
            total += (cart_item.producto.precio * cart_item.cantidad)
            cantidad += cart_item.cantidad
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass ## solo ignora la exception

    context = {
        'total': total,
        'cantidad': cantidad,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total': grand_total
    }

    return render(request, 'tienda/pagar.html', context)

    