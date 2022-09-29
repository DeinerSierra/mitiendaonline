from .models import Carro, CarroItem
from .views import _cart_id


def counter(request):
    cart_count = 0

    try:
        cart = Carro.objects.filter(carro_id=_cart_id(request))

        if request.user.is_authenticated:
            cart_items = CarroItem.objects.all().filter(usuario=request.user)
        else:
            cart_items = CarroItem.objects.all().filter(carro=cart[:1])

        for cart_item in cart_items:
            cart_count += cart_item.cantidad
    except Carro.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)
        