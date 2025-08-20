from django.urls import path
from . import views # Importa as views do app loja
from django.contrib.auth import views as auth_views

app_name = 'loja'

urlpatterns = [
    # Quando a URL for a raiz (''), chame a função 'home' da views.py
    # O 'name="home"' é um apelido útil para esta URL.
    path('', views.home, name='home'),
    # Adicione esta nova linha para a página de produtos
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('sobre/', views.sobre, name='sobre'),

    # Novas URLs de Autenticação
    path('cadastro/', views.cadastro, name='cadastro'),
    # A view de Login do Django espera um template em 'registration/login.html'
    path('login/', auth_views.LoginView.as_view(template_name='loja/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # <int:produto_id> captura o ID do produto da URL
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', views.detalhe_carrinho, name='detalhe_carrinho'),
    path('carrinho/remover/<str:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('pedido/finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('meus-pedidos/<int:pedido_id>/', views.detalhe_pedido, name='detalhe_pedido'),
    path('meus-enderecos/', views.lista_enderecos, name='lista_enderecos'),
    path('meus-enderecos/adicionar/', views.adicionar_endereco, name='adicionar_endereco'),
    path('checkout/', views.checkout, name='checkout'),
    path('produto/<slug:produto_slug>/', views.detalhe_produto, name='detalhe_produto'),
    path('meu-perfil/', views.perfil, name='perfil'),
    path(
        'alterar-senha/',
        auth_views.PasswordChangeView.as_view(
            template_name='loja/alterar_senha.html',
            success_url='/alterar-senha/sucesso/' # URL para redirecionar após sucesso
        ),
        name='alterar_senha'
    ),
    path(
        'alterar-senha/sucesso/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='loja/alterar_senha_sucesso.html'
        ),
        name='alterar_senha_sucesso'
    ),
]
