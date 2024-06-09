from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, iPhone
import requests
from validate_docbr import CPF

class iPhoneForm(forms.ModelForm):
    class Meta:
        model = iPhone
        fields = ['modelo', 'descricao', 'condicao', 'memoria_interna', 'cor', 'saude_bateria', 'preco_venda']
        labels = {
            'modelo': 'Modelo',
            'descricao': 'Descrição',
            'condicao': 'Condição',
            'memoria_interna': 'Memória Interna (GB)',
            'cor': 'Cor',
            'saude_bateria': 'Saúde da Bateria (%)',
            'preco_venda': 'Preço de Venda (R$)',
        }
        widgets = {
            'modelo': forms.Select(attrs={'id': 'id_modelo'}),
            'descricao': forms.Textarea(attrs={'id': 'id_descricao', 'maxlength': '400'}),
            'condicao': forms.Select(attrs={'id': 'id_condicao'}),
            'memoria_interna': forms.Select(attrs={'id': 'id_memoria_interna'}),
            'cor': forms.TextInput(attrs={'id': 'id_cor'}),
            'saude_bateria': forms.NumberInput(attrs={'id': 'id_saude_bateria'}),
            'preco_venda': forms.NumberInput(attrs={'id': 'id_preco_venda'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        condicao = cleaned_data.get('condicao')
        if condicao == 'Novo':
            cleaned_data['saude_bateria'] = None  # Definir como None para iPhones novos
        return cleaned_data

class iPhoneSearchForm(forms.Form):
    modelo = forms.ChoiceField(choices=iPhone.MODELO_CHOICES, required=False, label='Modelo')
    condicao = forms.ChoiceField(choices=iPhone.CONDICAO_CHOICES, required=False, label='Condição')
    memoria_interna = forms.ChoiceField(choices=iPhone.MEMORIA_CHOICES, required=False, label='Memória Interna (GB)')
    cor = forms.CharField(max_length=30, required=False, label='Cor')
    saude_bateria = forms.IntegerField(required=False, label='Saúde da Bateria (%)')

class CustomUserCreationForm(UserCreationForm):
    telefone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '(00) 0000-0000'}),
        label='Telefone (WhatsApp)'
    )
    cpf_cnpj = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
        label='CPF/CNPJ'
    )
    cep = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '00000-000'}),
        label='CEP'
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'nome_completo', 'nome_da_loja', 'email', 'cpf_cnpj',
            'telefone', 'instagram', 'cep', 'logradouro', 'numero',
            'complemento', 'bairro', 'cidade', 'uf', 'password1', 'password2'
        )
        labels = {
            'username': 'Nome de usuário',
            'nome_completo': 'Nome completo',
            'nome_da_loja': 'Nome da loja',
            'email': 'E-mail',
            'logradouro': 'Logradouro',
            'numero': 'Número',
            'complemento': 'Complemento',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'uf': 'UF',
            'password1': 'Senha',
            'password2': 'Confirmação de senha',
        }
        help_texts = {
            'username': 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.',
            'password1': 'Sua senha não pode ser muito semelhante a outras suas informações pessoais. Deve conter pelo menos 8 caracteres. Não pode ser uma senha comum. Não pode ser inteiramente numérica.',
        }
        error_messages = {
            'username': {
                'unique': "Um usuário com este nome de usuário já existe.",
            },
        }

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        cpf = CPF()
        if not cpf.validate(cpf_cnpj):
            raise forms.ValidationError('CPF inválido.')
        return cpf_cnpj

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if response.status_code != 200 or 'erro' in response.json():
            raise forms.ValidationError('CEP inválido.')
        return cep

    def save(self, commit=True):
        user = super().save(commit=False)
        cep = self.cleaned_data.get('cep')
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if response.status_code == 200:
            data = response.json()
            user.logradouro = data.get('logradouro', '')
            user.bairro = data.get('bairro', '')
            user.cidade = data.get('localidade', '')
            user.uf = data.get('uf', '')
        if commit:
            user.save()
        return user
