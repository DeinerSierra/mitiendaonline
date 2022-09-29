from django.urls import path

from .import views

app_name="carrito"

urlpatterns = [
    path('', views.carro, name='carro'),
    path('add_cart/<int:product_id>/', views.add_cart, name='agregar_prtoducto'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
]