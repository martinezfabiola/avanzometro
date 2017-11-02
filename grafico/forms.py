from django import forms
from .models import Documento
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validator import validate_file_extension

class DocumentForm(forms.ModelForm):
    documento = forms.FileField(validators=[validate_file_extension])
    class Meta:
        model = Documento
        fields = ('documento',)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Requerido.Ingrese su nombre')
    last_name = forms.CharField(max_length=30, help_text='Requerido.Ingrese su apellido')
    username = forms.EmailField(max_length=254, help_text='Requerido.Ingrese su correo electronico.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )
