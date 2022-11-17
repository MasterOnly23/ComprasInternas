from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class Producto(models.Model):

    categorias = (('Todos', 'Todos'), ('Accesorios','Accesorios'),
    ('Farmacia','Farmacia'), ('Cuidado de la Piel', 'Cuidado de la Piel'),
    ('Cuidado de la Salud','Cuidado de la Salud'), ('Cuidado Personal','Cuidado Personal'), 
    ('Bebes y Niños','Bebes y Niños'), ('Salud Sexual','Salud Sexual'))

    nombre = models.CharField(max_length=60)
    categoria = models.CharField(max_length=25 ,choices=categorias, null=False)
    precio = models.IntegerField()



    def __str__(self):
        return f'{self.nombre} --- {self.precio}'

