from django import forms
from .models import Endereco, Avaliacao
from django.contrib.auth.models import User


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        # Define os campos do modelo que NÃO queremos no formulário.
        # O usuário será definido automaticamente na view.
        exclude = ('usuario',)

class UserUpdateForm(forms.ModelForm):
    # O campo email é obrigatório
    email = forms.EmailField()

    class Meta:
        model = User
        # Define os campos do modelo que queremos no formulário
        fields = ['username', 'email', 'first_name', 'last_name']


# Novo formulário para Avaliações
class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        # Apenas os campos que o usuário preencherá
        fields = ['nota', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }