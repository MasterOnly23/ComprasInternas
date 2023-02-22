from django import forms
from tienda.models import Pedido



class ContactForm(forms.Form):
    from_email = forms.EmailField(label="Email",required=True)
    subject = forms.CharField(label="Asunto",required=True)
    message = forms.CharField(label="Mensaje",widget=forms.Textarea(attrs={'rows':80, 'cols':48}), required=True)
    archivos = forms.FileField(label="Adjuntar Archivo", required=False)



class EditPedidoForm(forms.ModelForm):
    
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {'fecha_creacion': forms.DateInput(attrs={'type':'date'})}