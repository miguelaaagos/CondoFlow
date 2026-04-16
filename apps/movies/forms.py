from django import forms
from .models import Pago, Reserva, Unidad, Bloque, Anuncio


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'


class UnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ['name', 'numero', 'bloque', 'propietario', 'usuario']


class BloqueForm(forms.ModelForm):
    class Meta:
        model = Bloque
        fields = ['name', 'numero_pisos']


class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['name', 'contenido', 'destacado']


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contrasena')
