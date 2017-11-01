from django import forms
from .models import Documento

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ('documento',)