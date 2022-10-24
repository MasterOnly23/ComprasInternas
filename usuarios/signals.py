from django.db.models.signals import post_save
from .models import Profile, Usuarios
from django.dispatch import receiver

@receiver(post_save,sender=Usuarios) #decorador para llamar a la funcion
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)