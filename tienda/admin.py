from django.contrib import admin
from tienda.models import *
# Register your models here.


class BuscarAdminProducto(admin.ModelAdmin):
    # con esto muestras los campos que deses al mostrar la lista en admin
    list_display=['codProducto', 'categoria','descProducto', 'producto', 'precio', 'stockProducto', 'imagen']
    # con esto añades un campo de texto que te permite realizar la busqueda, puedes añadir mas de un atributo por el cual se filtrará
    search_fields = ['categoria', 'descProducto', 'id', 'codProducto', 'producto']
    # con esto añadiras una lista desplegable con la que podras filtrar (activo es un atributo booleano)
    list_filter = ['categoria']
    list_display_links = ['codProducto', 'categoria', 'descProducto', 'producto']
    list_per_page = 30

class BuscarAdminPedido(admin.ModelAdmin):
    
    # con esto muestras los campos que deses al mostrar la lista en admin
    list_display=['relacion_orden',  'codProducto', 'nombre', 'cantidad', 'acumulado']
    # # con esto añades un campo de texto que te permite realizar la busqueda, puedes añadir mas de un atributo por el cual se filtrará
    search_fields = [ 'nombre', 'nroPedido_id', 'codProducto', 'producto_id']
    # # con esto añadiras una lista desplegable con la que podras filtrar (activo es un atributo booleano)
    list_filter = ['nroPedido_id']
    # #ordering = ['para ordenar']
    # # list_editable = ['estado']
    list_display_links = ['relacion_orden','codProducto', 'nombre']
    list_per_page = 15 #(crea paginacion custom)
    #exclude(se listan pero no se pueden modificar)
    autocomplete_lookup_fields = {
        'nombre': ['nombre'],
        }


    def relacion_orden(self, obj):
        return obj.nroPedido.id
    relacion_orden.short_description = 'Numero Orden'


class BuscarAdminOrden(admin.ModelAdmin):
    # con esto muestras los campos que deses al mostrar la lista en admin
    list_display=['id',  'usuario', 'legajo', 'totalCarrito', 'fecha_creacion', 'estado']
    # con esto añades un campo de texto que te permite realizar la busqueda, puedes añadir mas de un atributo por el cual se filtrará
    search_fields = [ 'usuario', 'id', 'legajo', 'estado']
    # con esto añadiras una lista desplegable con la que podras filtrar (activo es un atributo booleano)
    list_filter = ['usuario', 'fecha_creacion', 'estado', 'legajo']
    #ordering = ['para ordenar']
    list_editable = ['estado']
    list_display_links = ['id', 'usuario', 'legajo']
    list_per_page = 15 #(crea paginacion custom)



class AdminDestacados(admin.ModelAdmin):
    # con esto muestras los campos que deses al mostrar la lista en admin
    list_display=['user', 'producto_id', 'acumulador']
    # con esto añades un campo de texto que te permite realizar la busqueda, puedes añadir mas de un atributo por el cual se filtrará
    search_fields = ['user', 'producto_id', 'acumulador']
    # con esto añadiras una lista desplegable con la que podras filtrar (activo es un atributo booleano)
    list_filter = ['user']
    #ordering = ['para ordenar']
    # list_editable = ['estado']
    list_display_links = ['user', 'producto_id', 'acumulador']
    list_per_page = 15 #(crea paginacion custom)




admin.site.register(TiendaProductos, BuscarAdminProducto)
admin.site.register(Pedido, BuscarAdminPedido)
admin.site.register(Orden, BuscarAdminOrden)
admin.site.register(ProductosDestacados, AdminDestacados)



class FilterWithCustomTemplate(admin.SimpleListFilter):
    template = "administrador/lista_pedidos.html"