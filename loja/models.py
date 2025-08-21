from django.db import models
from django.contrib.auth.models import User # Importa o modelo de usuário
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User # Importa o modelo de usuário
from decimal import Decimal


# Model para as Categorias dos produtos
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text='Nome da categoria')
    slug = models.SlugField(max_length=100, unique=True, help_text='Identificador único para a URL da categoria')

    class Meta:
        verbose_name_plural = "Categorias" # Define o nome plural no admin

    def __str__(self):
        # O __str__ define como o objeto será exibido (ex: no painel admin)
        return self.nome

# Model para os Produtos
class Produto(models.Model):
    nome = models.CharField(max_length=200, help_text='Nome do produto')
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField(help_text='Descrição detalhada do produto')
    # Usamos DecimalField para preços para evitar problemas de arredondamento
    preco = models.DecimalField(max_digits=10, decimal_places=2, help_text='Preço do produto')
    # ForeignKey cria a relação com a Categoria.
    # on_delete=models.CASCADE significa que se uma categoria for deletada,
    # todos os produtos nela também serão.
    categoria = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.CASCADE)
    estoque = models.PositiveIntegerField(default=0, help_text='Quantidade em estoque')
    disponivel = models.BooleanField(default=True, help_text='Indica se o produto está disponível para venda')
    # ImageField precisa da biblioteca Pillow. Instale com: pip install Pillow
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True, help_text='Imagem do produto')

    def __str__(self):
        return self.nome

class Endereco(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enderecos')
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, help_text="Sigla do estado, ex: SP")
    cep = models.CharField(max_length=9, help_text="Formato: 00000-000")
    padrao = models.BooleanField(default=False, help_text="Marcar como endereço principal")

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.cidade}, {self.estado}"


# Novo modelo para o Pedido
class Pedido(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('em_preparacao', 'Em Preparação'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    )
    endereco_entrega = models.ForeignKey(
        Endereco,
        on_delete=models.SET_NULL,  # Se o endereço for deletado, o pedido não será. O campo ficará nulo.
        null=True,  # Permite que o campo seja nulo no banco (para pedidos antigos sem endereço)
        blank=True  # Permite que o campo esteja em branco nos formulários
    )

    # Liga o pedido a um usuário. Se o usuário for deletado, seus pedidos também serão.
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True) # Data e hora da criação do pedido
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"

# Novo modelo para os Itens de um Pedido
class ItemPedido(models.Model):
    # Liga o item a um pedido. Se o pedido for deletado, os itens também serão.
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    # Liga o item a um produto. Se o produto for deletado, o item não será (para manter o histórico).
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no Pedido {self.pedido.id}"

    @property
    def subtotal(self):
        return self.preco * self.quantidade


