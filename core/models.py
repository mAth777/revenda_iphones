from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    nome_completo = models.CharField(max_length=150)
    nome_da_loja = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=20)
    telefone = models.CharField(max_length=15)
    instagram = models.CharField(max_length=50, blank=True)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return self.username

class iPhone(models.Model):
    MODELO_CHOICES = [
        ('iPhone 8', 'iPhone 8'),
        ('iPhone 8 Plus', 'iPhone 8 Plus'),
        ('iPhone X', 'iPhone X'),
        ('iPhone XR', 'iPhone XR'),
        ('iPhone XS', 'iPhone XS'),
        ('iPhone XS Max', 'iPhone XS Max'),
        ('iPhone 11', 'iPhone 11'),
        ('iPhone 11 Pro', 'iPhone 11 Pro'),
        ('iPhone 11 Pro Max', 'iPhone 11 Pro Max'),
        ('iPhone SE (2ª geração)', 'iPhone SE (2ª geração)'),
        ('iPhone 12', 'iPhone 12'),
        ('iPhone 12 Mini', 'iPhone 12 Mini'),
        ('iPhone 12 Pro', 'iPhone 12 Pro'),
        ('iPhone 12 Pro Max', 'iPhone 12 Pro Max'),
        ('iPhone 13', 'iPhone 13'),
        ('iPhone 13 Mini', 'iPhone 13 Mini'),
        ('iPhone 13 Pro', 'iPhone 13 Pro'),
        ('iPhone 13 Pro Max', 'iPhone 13 Pro Max'),
        ('iPhone 14', 'iPhone 14'),
        ('iPhone 14 Plus', 'iPhone 14 Plus'),
        ('iPhone 14 Pro', 'iPhone 14 Pro'),
        ('iPhone 14 Pro Max', 'iPhone 14 Pro Max'),
        ('iPhone 15', 'iPhone 15'),
        ('iPhone 15 Plus', 'iPhone 15 Plus'),
        ('iPhone 15 Pro', 'iPhone 15 Pro'),
        ('iPhone 15 Pro Max', 'iPhone 15 Pro Max'),
    ]
    
    CONDICAO_CHOICES = [
        ('Novo', 'Novo'),
        ('Seminovo', 'Seminovo'),
    ]

    MEMORIA_CHOICES = [
        ('64GB', '64GB'),
        ('128GB', '128GB'),
        ('256GB', '256GB'),
        ('512GB', '512GB'),
        ('1TB', '1TB'),
    ]

    modelo = models.CharField(max_length=50, choices=MODELO_CHOICES)
    descricao = models.TextField(max_length=400)
    condicao = models.CharField(max_length=10, choices=CONDICAO_CHOICES)
    memoria_interna = models.CharField(max_length=10, choices=MEMORIA_CHOICES)
    cor = models.CharField(max_length=30)
    saude_bateria = models.IntegerField(null=True, blank=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    fornecedor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.modelo} ({self.memoria_interna}) - {self.condicao}'
