from django.contrib import admin
from .models import Categoria, Produto, Pedido, ItemPedido

# --- Customização para Produtos e Categorias ---
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)} # Preenche o slug automaticamente

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'estoque', 'disponivel')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descricao')

# --- Customização para Pedidos ---

# Esta classe permite que os Itens do Pedido sejam exibidos e editados
# DENTRO da página de detalhes de um Pedido.
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    # 'extra = 0' impede que campos extras para novos itens sejam exibidos por padrão.
    extra = 0
    # Define campos que não podem ser editados (readonly).
    readonly_fields = ('produto', 'preco', 'quantidade')


# Esta é a customização principal para o modelo Pedido.
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Campos a serem exibidos na lista de pedidos.
    list_display = ('id', 'usuario', 'criado_em', 'status', 'total')
    # Filtros que aparecerão na barra lateral direita.
    list_filter = ('status', 'criado_em')
    # Campos pelos quais você poderá buscar.
    search_fields = ('usuario__username', 'id')

    # AQUI A MÁGICA ACONTECE:
    # Informamos ao admin do Pedido para incluir a visualização inline dos Itens.
    inlines = [ItemPedidoInline]

    # Define campos que serão apenas de leitura na tela de detalhes.
    # Evita que o admin altere acidentalmente dados que são calculados automaticamente.
    readonly_fields = ('usuario', 'criado_em', 'total')


# Não precisamos mais do admin.site.register() simples, pois usamos o decorator @admin.register.