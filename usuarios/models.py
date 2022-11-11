from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
# Create your models here.




# class Usuarios(AbstractUser):

#     email = models.EmailField('Direccion email', unique=True)
#     username = models.CharField('Repetir email', max_length=50)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=80)

#     #areas de trabajo
#     areas = (('Administracion','Administracion'),('Sistemas','Sistemas'),('Imagen','Imagen'),('RRHH','RRHH'), ('Abastecimiento','Abastecimiento'),
#     ('Mantenimiento','Mantenimiento'),('Gerentes','Gerentes'), ('Compras','Compras'), ('Legales','Legales'), ('Otra','Otra'))
#     area = models.CharField(max_length=20 ,choices=areas, null=False)


#     #tipo de usuario
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username','first_name','last_name', 'area']


# class Profile(models.Model):
#     user = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='avatares' ,default="default.png", blank=True)


#     def __str__(self) -> str:
#         return f'Perfil de {self.user.email}'