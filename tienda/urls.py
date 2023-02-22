"""ComprasInternas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tienda.views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', index, name='index'),
    path('perfil/', perfil, name='perfil'),
    path('contacto/', contact_form, name='contacto'),

    path('agregar/<int:producto_id>/', agregar_producto, name="add"),
    path('restar/<int:producto_id>/', restar_producto, name="restar"),
    path('eliminar/<int:producto_id>/', elminar_producto, name="del"),
    path('limpiar/', limpiar_carrito, name="limpiar"),
    path('enviar/', pedido_mail, name="enviar_pedido"),

    path('buscar/<str:nombreProd>/', buscarProducto, name="buscarProducto"),

    path('categoria/<str:categoria>/', buscarCategoria, name="categoria"),


    path('listaOrden/', misPedidos, name="misPedidos"),
    path('listaPedidos/cancelar/<int:id_orden>/', cancelarPedido, name="cancelarPedido"),

    path('listaPedidos/<str:estado>/', filtroEstado, name="filtroEstado"),

    path('listaOrden/Pedidos/<int:nro_orden>/', pedidosOrden, name="pedidosOrden"),


    #ADMINISTRACION----
    # path('listaPedidos/', AdministradorView.listaPedidos, name="listaPedidos"),
    # path('editarPedido/<int:id_pedido>/', AdministradorView.editarPedido, name="editPedido"),
    # path('actualizarPedido/<int:id_pedido>/', AdministradorView.actualizarPedido, name="actualizarPedido"),
    # path('eliminarPedido/<int:id_pedido>/', AdministradorView.eliminar_pedido, name="eliminarPedido"),

    # #filtros
    # path('listaPedidos/filterUser/<int:id_user>/', AdministradorView.filtroUsuario, name="filtroUsuario"),
    # path('listaPedidos/filterUser/<str:rango>/<int:id_user>/', AdministradorView.filtroFechaUsuario, name="filtroFechaUsuario"),

    # path('listaPedidos/filterUser/<int:id_user>/<str:rango>/', AdministradorView.filtroUsuarioFecha, name="filtroUsuarioFecha"),

    path('listaPedidos/filterDate/<str:rango>/', AdministradorView.filtroFecha, name="filtroFecha"),
    # path('listaPedidos/filterDate/<int:id_user>/<str:rango>/', AdministradorView.filtroFecha, name="filtroFechaUser"),





    # path('carrito/', carrito, name="carrito"),
    



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



