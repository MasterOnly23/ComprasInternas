from datetime import datetime
from django.core.mail import send_mail, BadHeaderError
from decimal import Decimal


class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]

        else:
            self.carrito = carrito


    def agregar_prod_farmacia(self, producto):
        id = str(producto.id)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "producto_id": producto.id,
                "codigo_producto": producto.codProducto,
                "nombre" : producto.descProducto,
                "precio" : float(producto.precio),
                "acumulado" : float(producto.precio) * 0.7,
                "cantidad": 1,

            }



        else: 
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += (float(producto.precio) * 0.7)
        self.guardar_carrito()

    
    def agregar_prod_accesorios(self, producto):
        id = str(producto.id)
        if id not in self.carrito.keys():

                self.carrito[id] = {
                    "producto_id": producto.id,
                    "codigo_producto": producto.codProducto,
                    "nombre" : producto.descProducto,
                    "precio" : float(producto.precio),
                    "acumulado" : float(producto.precio) * 0.85,
                    "cantidad": 1,

                }


        else: 
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += (float(producto.precio) * 0.85)
        self.guardar_carrito()

    
    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()
    
    def restarFarmacia(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= (float(producto.precio) * 0.7)
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.guardar_carrito()


    def restarAccesorios(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= (float(producto.precio) * 0.85)
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
        

    def lista_carrito(self, producto):
        id = str(producto.id)
        self.carrito[id] = {
                "producto_id": producto.id,
                "nombre" : producto.descProducto,
                "precio" : float(producto.precio),
                "acumulado" : float(producto.precio),
                "cantidad": 1,

            }
        self.guardar_carrito()
        return self.carrito[id]





    