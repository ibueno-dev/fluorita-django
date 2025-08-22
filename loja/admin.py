from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _ # Importante para os fieldsets
from .models import Categoria, Produto, ItemPedido, Pedido, Avaliacao


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
    # Para preencher o slug automaticamente
    prepopulated_fields = {'slug': ('nome',)}

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


class CustomUserAdmin(UserAdmin):
    """
    Substitui a classe UserAdmin padrão para remover o campo de senha.
    """
    # Redefinimos os fieldsets, copiando o padrão do Django mas
    # removendo 'password' da primeira linha.
    fieldsets = (
        # A linha original era: (None, {'fields': ('username', 'password')})
        (None, {'fields': ('username', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'usuario', 'nota', 'criado_em')
    list_filter = ('nota', 'criado_em')
    search_fields = ('produto__nome', 'usuario__username', 'comentario')



# Desregistra o UserAdmin padrão do Django
admin.site.unregister(User)
# Registra o User novamente com a nossa classe customizada
admin.site.register(User, CustomUserAdmin)
