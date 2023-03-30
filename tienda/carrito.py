from datetime import datetime
from django.core.mail import send_mail, BadHeaderError
from decimal import Decimal


import json
from datetime import timedelta
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone

class Carrito:
    COOKIE_NAME = "carrito_compras"  # nombre de la cookie

    def __init__(self, request):
        self.request = request
        self.cookie_cart = self.get_cookie_cart()  # obtiene la cookie si existe


        if not self.cookie_cart:
            self.cart = {}  # si la cookie no existe, se inicializa un carrito vacío
        else:
            self.cart = json.loads(self.cookie_cart)  # si la cookie existe, se carga su contenido en el carrito
            print('Contenido de la cookie cargado:', self.cart)
            self.set_cookie_cart()  # actualiza la cookie con el contenido del carrito

    def get_cookie_cart(self):
        return self.request.COOKIES.get(self.COOKIE_NAME)  # obtiene el valor de la cookie

    def set_cookie_cart(self):
        cart_json = json.dumps(self.cart)  # convierte el carrito en un string JSON
        #expires = timezone.now() + timedelta(days=settings.CART_COOKIE_EXPIRATION)  # establece la fecha de expiración de la cookie
        expiry = datetime.utcnow() + timedelta(days=8)
        response = HttpResponse()
        response.set_cookie(key=self.COOKIE_NAME, value=cart_json, expires=expiry, httponly=True)      
        print('Cookie actualizada:', self.cart)
        return response
        # crea o actualiza la cookie con el contenido del carrito

    def agregar_prod_farmacia(self, producto):
        id = str(producto.id)
        if id not in self.cart.keys():  # si el producto no está en el carrito, se agrega
            self.cart[id] = {
                "producto_id": producto.id,
                "codigo_producto": producto.codProducto,
                "nombre" : producto.descProducto,
                "precio" : float(producto.precio),
                "acumulado" : float(producto.precio) * 0.7,  # se aplica un descuento del 30% para productos de farmacia
                "cantidad": 1,
            }
            print('agregado')

        else:  # si el producto ya está en el carrito, se aumenta la cantidad y se recalcula el acumulado
            self.cart[id]["cantidad"] += 1
            self.cart[id]["acumulado"] += (float(producto.precio) * 0.7)
        self.set_cookie_cart()  # actualiza la cookie con el contenido del carrito

    def agregar_prod_accesorios(self, producto):
        id = str(producto.id)
        if id not in self.cart.keys():  # si el producto no está en el carrito, se agrega
            self.cart[id] = {
                "producto_id": producto.id,
                "codigo_producto": producto.codProducto,
                "nombre" : producto.descProducto,
                "precio" : float(producto.precio),
                "acumulado" : float(producto.precio) * 0.85,  # se aplica un descuento del 15% para productos de accesorios
                "cantidad": 1,
            }
            

        else:  # si el producto ya está en el carrito, se aumenta la cantidad y se recalcula el acumulado
            self.cart[id]["cantidad"] += 1
            self.cart[id]["acumulado"] += (float(producto.precio) * 0.85)
        self.set_cookie_cart()  # actualiza la cookie con el contenido del carrito




    def restarFarmacia(self, producto):
        id = str(producto.id)
        if id in self.cart.keys():
            self.cart[id]["cantidad"] -= 1
            self.cart[id]["acumulado"] -= (float(producto.precio) * 0.7)
            if self.cart[id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.set_cookie_cart()  # actualiza la cookie con el contenido del carrito


    def restarAccesorios(self, producto):
        id = str(producto.id)
        if id in self.cart.keys():
            self.cart[id]["cantidad"] -= 1
            self.cart[id]["acumulado"] -= (float(producto.precio) * 0.85)
            if self.cart[id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.set_cookie_cart()  # actualiza la cookie con el contenido del carrito


    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.cart.keys():
            del self.cart[id]
        self.set_cookie_cart()  # actualiza la cookie con el contenido del carrito


    # def lista_carrito(self, producto):
    #     id = str(producto.id)
    #     self.carrito[id] = {
    #             "producto_id": producto.id,
    #             "nombre" : producto.descProducto,
    #             "precio" : float(producto.precio),
    #             "acumulado" : float(producto.precio),
    #             "cantidad": 1,

    #         }
    #     self.guardar_carrito()
    #     return self.carrito[id]
    