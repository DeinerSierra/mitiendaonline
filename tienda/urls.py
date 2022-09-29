from django.urls import path
from . import views
app_name ='tienda'
urlpatterns = [
    path('', views.store, name="tienda"),
    path('categoria/<slug:categoria_slug>/', views.tienda_productos, name='categoria_productos'),
    path('categoria/<slug:categoria_slug>/<slug:producto_slug>/', views.detalle_producto, name='detalle_producto'),
    path('buscar/', views.buscar_producto, name='buscar_producto'),
    
]


