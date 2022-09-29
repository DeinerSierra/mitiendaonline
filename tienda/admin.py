from django.contrib import admin
from .models import Categoria, Producto, Variedad

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['categoria_nombre', 'slug']
    prepopulated_fields = {'slug':('categoria_nombre',)}
    
    
@admin.register(Producto)    
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('producto_nombre','precio','categoria','modified_date','disponible')
    list_filter = ['disponible','created_date','modified_date']
    list_editable = ['precio','disponible']
    prepopulated_fields = {'slug': ('producto_nombre',)}
    
@admin.register(Variedad)
class VariedadAdmin(admin.ModelAdmin):
    list_display = ('producto','variedad_categoria','variedad_valor','is_active','created_date')
    list_filter = ['producto','variedad_categoria','variedad_valor','is_active']
    #list_editable = ['created_date']
    



