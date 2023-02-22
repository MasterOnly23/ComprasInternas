from django.db.models.signals import post_save
from .models import Area, Legajo
from django.contrib.auth.models import User
from django.dispatch import receiver

# @receiver(post_save,sender=Usuarios) #decorador para llamar a la funcion
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

@receiver(post_save,sender=User) #decorador para llamar a la funcion
def asignar_area(sender, instance, created, **kwargs):
    if created:
        Area.objects.create(user=instance)
        Legajo.objects.create(user=instance)
