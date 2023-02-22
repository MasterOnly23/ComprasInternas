from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser

from allauth.account.models import allauth_app_settings
# from usuarios.forms import MyCustomSignupForm
# Create your models here.


class Area(models.Model):

    areas = (('None','None'),('Administracion','Administracion'),('Sistemas','Sistemas'),('Imagen','Imagen'),('RRHH','RRHH'), ('Abastecimiento','Abastecimiento'),
    ('Mantenimiento','Mantenimiento'),('Gerentes','Gerentes'), ('Compras','Compras'), ('Legales','Legales'), ('Deposito','Deposito'), ('Otra','Otra'))

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    area = models.CharField('Area', max_length=25, choices=areas, null=True, blank=True)


    def __str__(self) -> str:
        return f'{self.area}'


class Legajo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    legajo = models.CharField('Legajo', max_length=5, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.legajo}'



# class Usuarios(AbstractBaseUser):
#     id = models.IntegerField(primary_key=True, default='some_value')
#     first_name = models.CharField(max_length=100, null=True)
#     last_name = models.CharField(max_length=100, null=True)
#     email = models.EmailField(max_length=150, unique=True, null=True)


#     areas = (('None','None'),('Administracion','Administracion'),('Sistemas','Sistemas'),('Imagen','Imagen'),('RRHH','RRHH'), ('Abastecimiento','Abastecimiento'),
#     ('Mantenimiento','Mantenimiento'),('Gerentes','Gerentes'), ('Compras','Compras'), ('Legales','Legales'), ('Otra','Otra'))

#     area = models.CharField('Area', max_length=25, choices=areas, null=False)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["first_name", "last_name"]

#     def get_short_name(self):
#         return self.first_name

#     def get_full_name(self):
#         return "%s %s" % (self.first_name, self.last_name)


#     def __str__(self) -> str:
#         return f'{self.area}'


#     class Meta:
#         swappable = "AUTH_USER_MODEL"



# class User(AbstractUser):

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