from django import forms
from django.contrib.auth.forms import UserChangeForm
from allauth.account.forms import SignupForm
from allauth.account.models import allauth_app_settings
from usuarios.models import Area, Legajo

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

from allauth.account.forms import ChangePasswordForm



class EditArea(forms.ModelForm):


    areas = (('None','None'),('Administracion','Administracion'),('Sistemas','Sistemas'),('Imagen','Imagen'),('RRHH','RRHH'), ('Abastecimiento','Abastecimiento'),
    ('Mantenimiento','Mantenimiento'),('Gerentes','Gerentes'), ('Compras','Compras'), ('Legales','Legales'), ('Otra','Otra'))
    area = forms.ChoiceField(choices=areas)


    class Meta:
        model = Area
        fields = ['area']


areas = (('None','None'),('Administracion','Administracion'),('Sistemas','Sistemas'),('Imagen','Imagen'),('RRHH','RRHH'), ('Abastecimiento','Abastecimiento'),
    ('Mantenimiento','Mantenimiento'),('Gerentes','Gerentes'), ('Compras','Compras'), ('Legales','Legales'), ('Otra','Otra'))

class EditLegajo(forms.ModelForm):

    legajo = forms.CharField()

    class Meta:
        model = Legajo
        fields = ['legajo']




class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label="Nombre", max_length=100)
    last_name = forms.CharField(label="Apellido", max_length=100)
    username = forms.EmailField(label="Repetir Email")
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput, max_length=15)
    password2 = forms.CharField(label="Repetir Contraseña", widget=forms.PasswordInput, max_length=15)
    # area = forms.ChoiceField(choices=areas, required=True)

    # class Meta:
    #     model = User
    #     fields = ['first_name','last_name','username', 'email', 'password1', 'password2', 'area']
    #     help_texts = {k:"" for k in fields}


    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        user.area = self.cleaned_data['area']
        user.save()
        return user



class CambiarContraseña(ChangePasswordForm):

    oldpassword = forms.CharField(label="Contraseña Actual", widget=forms.PasswordInput())
    password1 = forms.CharField(label="Nueva Contraseña", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Nueva Contraseña (De nuevo)", widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ['old_password', 'password1', 'password2']



class EditarDatosUsuario(UserChangeForm):
    first_name = forms.CharField(label="Nombre", max_length=100)
    last_name = forms.CharField(label="Apellido", max_length=100)
    password = forms.CharField(label="", required=None)
    

    class Meta:
        model = User
        fields = ['first_name','last_name']
        help_texts = {
            'username': None,
            'email': None,
        }



    # def signup(self, request, user):
    #     up = user.area
    #     up.area = self.cleaned_data['area']
    #     user.save()
    #     up.save


    # def __str__(self) -> str:
    #     return f'{self.user.area}'

#     # area = forms.CharField(max_length=25)

#     def save(self, request):

#         # Ensure you call the parent class's save.
#         # .save() returns a User object.
#         user = super(MyCustomSignupForm, self).save(commit=False)

#         # Add your own processing here.

#         # You must return the original result.
#         return user


#     class Meta:
#         model = allauth_app_settings.USER_MODEL
#         fields = ['area']
