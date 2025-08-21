from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Endereco
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from .models import Pedido, ItemPedido
from .forms import EnderecoForm, UserUpdateForm
from django.db import transaction


# Esta é a função que a nossa URL chama
def home(request):
    return render(request, 'loja/home.html')

def lista_produtos(request):
    # 1. A consulta ao banco de dados: Pega TODOS os objetos do modelo Produto.
    produtos = Produto.objects.all()

    # 2. O contexto: Um dicionário que leva os dados para o template.
    # A chave 'produtos' será o nome da variável no HTML.
    context = {
        'produtos': produtos
    }

    # 3. Renderiza o template, passando o contexto com os nossos produtos.
    return render(request, 'loja/lista_produtos.html', context)

def sobre(request):
    # Como a página é estática, apenas renderizamos o template.
    return render(request, 'loja/sobre.html')

def cadastro(request):
    if request.method == 'POST':
        # Se o formulário foi enviado, cria uma instância com os dados enviados
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Se o formulário é válido, salva o novo usuário no banco
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada com sucesso para {username}! Você já pode fazer o login.')
            # Redireciona o usuário para a página de login
            return redirect('loja:login')
    else:
        # Se a requisição for GET, apenas mostra um formulário em branco
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'loja/cadastro.html', context)

def adicionar_ao_carrinho(request, produto_id):
    # Garante que o produto existe antes de tentar adicioná-lo
    produto = get_object_or_404(Produto, id=produto_id)

    # Pega o carrinho da sessão atual, ou cria um dicionário vazio se não houver carrinho
    carrinho = request.session.get('carrinho', {})

    # Pega a quantidade do formulário (request.POST)
    quantidade = int(request.POST.get('quantidade', 1))

    produto_id_str = str(produto_id)

    # Lógica para adicionar ou atualizar a quantidade do produto no carrinho
    if produto_id_str in carrinho:
        carrinho[produto_id_str]['quantidade'] += quantidade
    else:
        carrinho[produto_id_str] = {
            'produto_id': produto_id,
            'nome': produto.nome,
            'preco': str(produto.preco), # Armazenamos como string para evitar problemas de serialização
            'quantidade': quantidade,
        }

    # Salva o carrinho de volta na sessão
    request.session['carrinho'] = carrinho

    # Redireciona o usuário de volta para a lista de produtos
    return redirect('loja:lista_produtos')

def detalhe_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    carrinho_detalhado = []
    total_carrinho = Decimal('0.00')

    # Itera sobre os itens no carrinho da sessão para processá-los
    for produto_id, item_data in carrinho.items():
        subtotal = Decimal(item_data['preco']) * int(item_data['quantidade'])
        total_carrinho += subtotal

        carrinho_detalhado.append({
            'produto_id': produto_id,
            'nome': item_data['nome'],
            'preco': Decimal(item_data['preco']),
            'quantidade': item_data['quantidade'],
            'subtotal': subtotal,
        })

    context = {
        'carrinho_detalhado': carrinho_detalhado,
        'total_carrinho': total_carrinho,
    }
    return render(request, 'loja/detalhe_carrinho.html', context)

def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id_str = str(produto_id) # Garante que a chave é uma string

    if produto_id_str in carrinho:
        del carrinho[produto_id_str]
        request.session['carrinho'] = carrinho # Salva as alterações na sessão

    return redirect('loja:detalhe_carrinho')

@login_required
def meus_pedidos(request):
    # Filtra os pedidos para pegar apenas os do usuário logado
    # e ordena pelos mais recentes primeiro.
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-criado_em')
    context = {
        'pedidos': pedidos
    }
    return render(request, 'loja/meus_pedidos.html', context)

@login_required
def detalhe_pedido(request, pedido_id):
    # A adição de 'usuario=request.user' aqui é uma medida de segurança CRUCIAL.
    # Garante que um usuário não possa ver o pedido de outro apenas adivinhando a URL.
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    context = {
        'pedido': pedido
    }
    return render(request, 'loja/detalhe_pedido.html', context)

@login_required
def lista_enderecos(request):
    enderecos = Endereco.objects.filter(usuario=request.user)
    return render(request, 'loja/lista_enderecos.html', {'enderecos': enderecos})

@login_required
def adicionar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            # Não salva o objeto ainda, pois precisamos adicionar o usuário
            endereco = form.save(commit=False)
            # Associa o endereço ao usuário logado
            endereco.usuario = request.user
            endereco.save()
            return redirect('loja:lista_enderecos')
    else:
        form = EnderecoForm()
    return render(request, 'loja/adicionar_endereco.html', {'form': form})

@login_required
def checkout(request):
    # Pega os endereços do usuário logado
    enderecos = Endereco.objects.filter(usuario=request.user)
    # Pega o carrinho da sessão para exibir um resumo
    carrinho = request.session.get('carrinho', {})

    if not carrinho:
        messages.error(request, "Seu carrinho está vazio.")
        return redirect('loja:lista_produtos')

    context = {
        'enderecos': enderecos,
        'carrinho': carrinho.values() # Passa os valores do carrinho para o template
    }
    return render(request, 'loja/checkout.html', context)

@login_required
def finalizar_pedido(request):
    # Verifica se o método é POST
    if request.method != 'POST':
        return redirect('loja:checkout') # Se não for POST, volta para a seleção de endereço

    carrinho = request.session.get('carrinho', {})
    endereco_id = request.POST.get('endereco_id')

    # Validações
    if not carrinho:
        messages.error(request, "Seu carrinho está vazio.")
        return redirect('loja:lista_produtos')
    if not endereco_id:
        messages.error(request, "Por favor, selecione um endereço de entrega.")
        return redirect('loja:checkout')

    try:
        endereco_selecionado = Endereco.objects.get(id=endereco_id, usuario=request.user)
    except Endereco.DoesNotExist:
        messages.error(request, "Endereço inválido.")
        return redirect('checkout')


    try:
        # A transação garante que todas as operações de banco de dados abaixo
        # ou funcionam todas juntas, ou nenhuma delas funciona.
        # Isso evita inconsistências (ex: criar pedido mas não atualizar o estoque).
        with transaction.atomic():
            # PASSO 1: Verificação de estoque ANTES de criar o pedido
            for produto_id, item_data in carrinho.items():
                produto = get_object_or_404(Produto, id=produto_id)
                quantidade_pedida = int(item_data['quantidade'])

                if produto.estoque < quantidade_pedida:
                    # Se um item não tiver estoque, interrompe tudo
                    messages.error(request,
                                   f"Desculpe, não temos estoque suficiente para '{produto.nome}'. Disponível: {produto.estoque}.")
                    return redirect('loja:detalhe_carrinho')  # Redireciona de volta para o carrinho

            # Se o loop acima terminar sem problemas, significa que há estoque para tudo.
            # Agora podemos continuar com a criação do pedido.

            # ... (a lógica de cálculo do total continua a mesma) ...
            total_carrinho = Decimal('0.00')
            for produto_id, item_data in carrinho.items():
                total_carrinho += Decimal(item_data['preco']) * int(item_data['quantidade'])

            # Cria o objeto Pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                total=total_carrinho,
                endereco_entrega=endereco_selecionado
            )

            # Cria os objetos ItemPedido E ATUALIZA o estoque
            for produto_id, item_data in carrinho.items():
                produto = get_object_or_404(Produto, id=produto_id)
                quantidade_pedida = int(item_data['quantidade'])

                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=produto,
                    preco=Decimal(item_data['preco']),
                    quantidade=quantidade_pedida
                )

                # PASSO 2: Dedução do estoque
                produto.estoque -= quantidade_pedida
                produto.save()  # Salva a nova quantidade no banco

    except Exception as e:
        # Em caso de qualquer outro erro inesperado, avisa o usuário.
        messages.error(request, f"Ocorreu um erro ao processar seu pedido: {e}")
        return redirect('loja:checkout')

        # --- FIM DA NOVA LÓGICA ---

        # Limpa o carrinho da sessão
    del request.session['carrinho']

    messages.success(request, f'Pedido #{pedido.id} realizado com sucesso!')
    return redirect('loja:meus_pedidos')

@login_required
def perfil(request):
    if request.method == 'POST':
        # Cria o formulário com os dados enviados E com a instância do usuário atual
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('loja:perfil') # Redireciona para a mesma página
    else:
        # Cria o formulário preenchido com os dados do usuário atual
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }
    return render(request, 'loja/perfil.html', context)

def detalhe_produto(request, produto_slug):
    # Busca o produto pelo slug ou retorna um erro 404 (Página não encontrada)
    produto = get_object_or_404(Produto, slug=produto_slug)
    context = {
        'produto': produto
    }
    return render(request, 'loja/detalhe_produto.html', context)

