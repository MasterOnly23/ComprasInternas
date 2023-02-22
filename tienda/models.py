from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from datetime import datetime

from django.conf import settings

from decimal import Decimal

# Create your models here.

estados = (('Entregado','Entregado'), ('Pendiente', 'Pendiente'), ('Cancelado', 'Cancelado'))


class Producto(models.Model):

    categorias = (('Todos', 'Todos'), ('Accesorios','Accesorios'),
    ('Farmacia','Farmacia'), ('Cuidado de la Piel', 'Cuidado de la Piel'),
    ('Cuidado de la Salud','Cuidado de la Salud'), ('Cuidado Personal','Cuidado Personal'), 
    ('Bebes y Niños','Bebes y Niños'), ('Salud Sexual','Salud Sexual'))

    nombre = models.CharField(max_length=60)
    categoria = models.CharField(max_length=25 ,choices=categorias, null=False)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    codProducto = models.CharField(max_length=4, null=True)
    nombreProducto = models.CharField(max_length=60, null=True)
    imagen = models.ImageField(upload_to='img-productos', default="default_prod.png", blank=True)


    def asignar_precio(self, precio_float):
        self.precio = Decimal(precio_float)

    def __str__(self):
        return f'{self.nombre} --- {self.precio} -- {self.imagen.url}'

    class Meta:
        managed = False
        db_table = 'tienda_producto'



class Orden(models.Model):


    legajo = models.CharField(max_length=5)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    usuario = models.CharField(max_length=100)
    totalCarrito = models.DecimalField(max_digits=7, decimal_places=2)
    fecha_creacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=10 ,choices=estados, default='Pendiente')
    #articulos = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True)

   
    class Meta:
        verbose_name_plural = "Ordenes"
        managed = False
        db_table = 'tienda_orden'

    def asignar_precio(self, precio_float):
        self.totalCarrito = Decimal(precio_float)

class Pedido(models.Model):
    fecha_hoy = datetime.today().strftime('%Y-%m-%d')


    nroPedido = models.ForeignKey(Orden, on_delete=models.CASCADE)
    
    
    producto_id = models.IntegerField(null=True)
    codProducto = models.CharField(max_length=4, null=True)
    nombre = models.CharField(max_length=60)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    acumulado = models.DecimalField(max_digits=7, decimal_places=2)
    cantidad = models.IntegerField()


    def asignar_precio(self, precio_float, acumulado):
        self.precio = Decimal(precio_float)
        self.acumulado = Decimal(acumulado)



    def __unicode__(self):
        return self.nroPedido_id
    
    @staticmethod
    def autocomplete_search_fields():
        return ("nombre__icontains",)


    def __str__(self):
        return f"Pedido Nro - {self.nroPedido.id} --> {self.codProducto} --- {self.nombre} --- {self.precio} -- {self.cantidad} --- {self.acumulado}"

    class Meta:
        managed = False
        db_table = 'tienda_pedido'

 
    

    #Modelos tablas bejerman

class TiendaArticulos(models.Model):
    id = models.IntegerField(primary_key=True)
    codigogenerico = models.CharField(db_column='codigoGenerico', max_length=20)  # Field name made lowercase.
    producto = models.CharField(max_length=50)
    precio = models.FloatField()
    fechmod = models.DateTimeField(db_column='FechMod')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tienda_articulos'


    
class TiendaStock(models.Model):
    id = models.IntegerField(primary_key=True)
    codigogenerico = models.CharField(db_column='codigoGenerico', max_length=20)  # Field name made lowercase.
    cantum1 = models.FloatField(db_column='cantUM1')  # Field name made lowercase.
    cantum2 = models.FloatField(db_column='cantUM2')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tienda_stock'


class TiendaStockproducto(models.Model):
    id = models.IntegerField(primary_key=True)
    codproducto = models.CharField(db_column='codProducto', max_length=4, blank=True, null=True)  # Field name made lowercase.
    producto = models.CharField(max_length=25, blank=True, null=True)
    codigogenerico = models.CharField(db_column='codigoGenerico', max_length=20)  # Field name made lowercase.
    descproducto = models.CharField(db_column='descProducto', max_length=50)  # Field name made lowercase.
    stockproducto = models.FloatField(db_column='stockProducto')  # Field name made lowercase.
    stockdescproducto = models.FloatField(db_column='stockDescProducto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tienda_stockProducto'
    


class TiendaProductos(models.Model):

    categorias = (('Accesorios','Accesorios'),
    ('Farmacia','Farmacia'))

    id = models.IntegerField(primary_key=True)
    codProducto = models.CharField(db_column='codProducto', max_length=4, blank=True, null=True)  # Field name made lowercase.
    producto = models.CharField(max_length=25, blank=True, null=True)
    codigoGenerico = models.CharField(db_column='codigoGenerico', max_length=20)  # Field name made lowercase.
    descProducto = models.CharField(db_column='descProducto', max_length=50)  # Field name made lowercase.
    stockProducto = models.FloatField(db_column='stockProducto')  # Field name made lowercase.
    precio = models.FloatField()
    fechMod = models.DateTimeField(db_column='fechMod')  # Field name made lowercase.
    imagen = models.ImageField(upload_to='img-productos', default="default_prod.png")
    categoria = models.CharField(max_length=25 ,choices=categorias, null=True)
    

    class Meta:
        managed = False
        db_table = 'tienda_productos'
        verbose_name = 'Producto'
        verbose_name_plural = "Productos"




class ProductosDestacados(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=None)
    producto = models.ForeignKey(TiendaProductos, on_delete=models.CASCADE, blank=True, null=True)
    acumulador = models.IntegerField(default=0)