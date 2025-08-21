# fluorita-django
# ✨ Fluorita E-commerce

![Status do Projeto](https://img.shields.io/badge/status-em%20desenvolvimento-yellowgreen)

Projeto de e-commerce completo desenvolvido com Django, simulando uma loja virtual de produtos como cristais e minerais. O sistema cobre todo o ciclo de vida de uma compra, desde a visualização dos produtos até a confirmação do pedido por e-mail.

## 🚀 Funcionalidades Implementadas

-   **Catálogo de Produtos:** Visualização de produtos organizados por categorias.
-   **Página de Detalhes do Produto:** Página dedicada para cada item com descrição, imagem e preço.
-   **Sistema de Autenticação Completo:** Cadastro, login e logout de usuários.
-   **Painel do Cliente:**
    -   Edição de informações de perfil (nome, e-mail).
    -   Alteração segura de senha.
    -   Histórico de pedidos com detalhes de cada compra.
    -   Gerenciamento de endereços de entrega.
-   **Carrinho de Compras:** Funcionalidade para adicionar, visualizar e remover itens, utilizando sessões do Django.
-   **Checkout Seguro:** Processo de finalização de compra com seleção de endereço para usuários logados.
-   **Gestão de Estoque:** Atualização automática do estoque após a finalização de um pedido.
-   **Notificações por E-mail:** Envio de e-mail de confirmação transacional após a realização de um pedido.
-   **Painel de Administração Otimizado:** Interface administrativa do Django customizada para gerenciamento eficiente de produtos, categorias e, principalmente, pedidos (com filtros, busca e visualização de itens do pedido).

## 🛠️ Tecnologias Utilizadas

-   **Backend:** Python 3, Django
-   **Banco de Dados:** MySQL
-   **Bibliotecas Python:** Pillow, python-decouple
-   **Frontend:** HTML (com Templates Django)

## ⚙️ Configuração do Ambiente de Desenvolvimento

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Pré-requisitos

-   Git
-   Python 3.10+
-   MySQL (ou MariaDB) Server

### 2. Clonando o Repositório

```bash
git clone git@github.com:ibueno-dev/fluorita-django.git
cd fluorita-django
```

### 3. Configuração do Banco de Dados (MySQL)

Você precisa criar um banco de dados e um usuário dedicado para o projeto.

1.  Acesse o terminal do MySQL:
    ```sql
    sudo mysql -u root -p
    ```

2.  Execute os seguintes comandos SQL para criar a base de dados e o usuário. Lembre-se de usar uma senha forte.

    ```sql
    -- Cria a base de dados com suporte a caracteres UTF-8 (importante para acentuação)
    CREATE DATABASE fluorita_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

    -- Cria o usuário 'fluorita' que só pode se conectar localmente
    CREATE USER 'fluorita'@'localhost' IDENTIFIED BY 'sua-senha-forte-aqui';

    -- Concede todos os privilégios ao usuário 'fluorita' sobre a base de dados 'fluorita-dev'
    GRANT ALL PRIVILEGES ON fluorita_dev.* TO 'fluorita'@'localhost';

    -- Aplica as alterações de privilégios
    FLUSH PRIVILEGES;

    -- Sai do terminal do MySQL
    EXIT;
    ```

### 4. Ambiente Virtual e Variáveis de Ambiente

É crucial usar um ambiente virtual para isolar as dependências do projeto.

1.  **Crie e ative o ambiente virtual:**
    ```bash
    # Cria a pasta .venv
    python -m venv .venv

    # Ativa o ambiente (Linux/macOS)
    source .venv/bin/activate
    ```

2.  **Crie o arquivo de variáveis de ambiente (`.env`):**
    Este arquivo guardará suas senhas e chaves secretas, e **não deve** ser enviado para o GitHub. Crie um arquivo chamado `.env` na raiz do projeto e preencha com o seguinte conteúdo:

    ```env
    # Chave secreta do Django (pode gerar uma nova se quiser)
    SECRET_KEY='sua-secret-key-do-settings.py'
    DEBUG=True

    # Configurações do Banco de Dados
    DB_NAME='fluorita-dev'
    DB_USER='fluorita'
    DB_PASSWORD='sua-senha-forte-aqui'
    DB_HOST='localhost'
    DB_PORT='3306'

    # Configurações de E-mail (Gmail)
    EMAIL_HOST_USER='seu_email@gmail.com'
    EMAIL_HOST_PASSWORD='sua_senha_de_app_de_16_letras'
    ```

    > **Como gerar a Senha de App do Gmail?**
    > 1.  Acesse sua Conta Google e ative a **"Verificação em Duas Etapas"**.
    > 2.  Vá para a página de **"Senhas de app"**: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
    > 3.  Selecione "Outro (nome personalizado)", digite "Projeto Django Fluorita" e clique em "Gerar".
    > 4.  Copie a senha de 16 letras gerada e cole no campo `EMAIL_HOST_PASSWORD`.

### 5. Instalação das Dependências

Com o ambiente virtual ativo, instale todas as bibliotecas listadas no arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 6. Migrações e Superusuário

1.  **Aplique as migrações** para criar todas as tabelas do projeto no banco de dados:
    ```bash
    python manage.py migrate
    ```

2.  **Crie uma conta de administrador** para acessar o painel `/admin/`:
    ```bash
    python manage.py createsuperuser
    ```

### 7. Executando o Servidor

Tudo pronto! Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Agora você pode acessar o site em [http://127.0.0.1:8000/](http://127.0.0.1:8000/) e o painel de administração em [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## 🗺️ Roadmap / Próximas Funcionalidades

O projeto possui uma base sólida, mas ainda há espaço para melhorias e novas funcionalidades:

-   [ ] **Integração de Gateway de Pagamento:** Implementar a comunicação com APIs como Mercado Pago ou PagSeguro.
-   [ ] **Estilização do Frontend:** Aplicar CSS e/ou um framework (como Bootstrap) para criar uma interface visualmente atraente.
-   [ ] **Ícones e Melhorias Visuais:** Utilizar bibliotecas como [Font Awesome](https://fontawesome.com/) para ícones.
-   [ ] **Sistema de Avaliações:** Permitir que os clientes avaliem os produtos.
-   [ ] **Carrinho de Compras Dinâmico:** Usar AJAX/JavaScript para que o carrinho seja atualizado sem recarregar a página.
-   [ ] **Deployment:** Preparar e implantar o projeto em um servidor de produção (ex: Heroku, DigitalOcean).

## 👤 Autor

**Isaac**

-   [GitHub](https://github.com/ibueno-dev)
-   [LinkedIn]()