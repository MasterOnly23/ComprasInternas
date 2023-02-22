from django.contrib import admin

from django.contrib import admin
from usuarios.models import Area, Legajo
# from usuarios.models import Usuarios
# Register your models here.


class BuscarAdminLegajo(admin.ModelAdmin):
    # con esto muestras los campos que deses al mostrar la lista en admin
    list_display=['user', 'legajo']
    # con esto añades un campo de texto que te permite realizar la busqueda, puedes añadir mas de un atributo por el cual se filtrará
    search_fields = ['legajo', 'user']
    list_display_links = ['legajo', 'user']


class BuscarAdminArea(admin.ModelAdmin):
    # con esto muestras los campos que deses al mostrar la lista en admin
    list_display=['user', 'area']
    # con esto añades un campo de texto que te permite realizar la busqueda, puedes añadir mas de un atributo por el cual se filtrará
    search_fields = ['area', 'user']
    list_display_links = ['area', 'user']


admin.site.register(Area, BuscarAdminArea)
admin.site.register(Legajo, BuscarAdminLegajo)
# admin.site.register(Profile)