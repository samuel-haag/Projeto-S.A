import tkinter as tk  # Importa a biblioteca tkinter para criar a interface gráfica
from tkinter import ttk, messagebox  # Importa ttk para Widgets avançados e caixas de diálogo
import json  # Importa a manipulação de dados em formato JSON

# Função para realizar o login
def realizar_login():
    usuario = entry_usuario.get()  # Obtém o nome de usuário inserido
    senha = entry_senha.get()  # Obtém a senha inserida
    try:
        with open("usuarios.json", "r") as f:  # Abre o arquivo de usuários
            usuarios = json.load(f)  # Carrega os dados do arquivo JSON
    except FileNotFoundError:  # Se o arquivo não existir
        usuarios = {}  # inicializa um dicionário vazio do (usuário)
    if usuario in usuarios and usuarios[usuario] == senha:  # Verifica credenciais do usuário e senha
        messagebox.showinfo("Login", "Login realizado com sucesso!")  # Mostra mensagem de sucesso
        abrir_tela_estoque()  # Abre a tela principal (gerenciamento de estoque)
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")  # Mostra mensagem de erro

# Função para realizar cadastro
def realizar_cadastro():
    usuario = entry_usuario.get()  # Obtém o nome do usuário
    senha = entry_senha.get()  # Obtém a senha
    try:
        with open("usuarios.json", "r") as f:  # Abre o arquivo de usuários
            usuarios = json.load(f)
    except FileNotFoundError:  # Se o arquivo não existir
        usuarios = {}
    if usuario in usuarios:  # Verifica se o usuário já existe
        messagebox.showerror("Erro", "Usuário já existe.")
        return
    usuarios[usuario] = senha  # Adiciona novo usuário
    with open("usuarios.json", "w") as f:  # Salva o dicionário atualizado
        json.dump(usuarios, f)
    messagebox.showinfo("Cadastro", f"Usuário '{usuario}' cadastrado com sucesso!")

# Função para abrir a tela principal
def abrir_tela_estoque():
    janela.destroy()  # Fecha a janela de login
    clientes = []  # Lista para armazenar os clientes
    estoque = tk.Tk()  # Cria a janela para o gerenciamento de estoque
    estoque.title("Controle de Estoque e Clientes - Produtos de Limpeza")  # Define o título da janela.
    estoque.configure(bg="#191970")  # Define a cor de fundo da janela.

    produtos = []  # Lista para armazenar os produtos.
    produto_id_counter = 1  # Contador para gerar IDs únicos para os produtos.

    # Função para adicionar um produto ao estoque.
    def adicionar_produto():
        nome = entry_nome_produto.get()  # Obtém o nome do produto.
        quantidade = entry_quantidade.get()  # Obtém a quantidade do produto.
        preco = entry_preco.get()  # Obtém o preço do produto.

        if not nome or not quantidade or not preco:  # Verifica se todos os campos foram preenchidos.
            label_resultado_produto.config(text="Por favor, preencha todos os campos do produto.")
            return

        try:
            quantidade = int(quantidade)  # Converte a quantidade para inteiro.
            preco = float(preco)  # Converte o preço para ponto flutuante.
            nonlocal produto_id_counter  # Acessa a variável global.
            produtos.append({"id": produto_id_counter, "nome": nome, "quantidade": quantidade, "preco": preco})  # Adiciona o produto à lista.
            produto_id_counter += 1  # Incrementa o contador de IDs.
            label_resultado_produto.config(text="Produto adicionado com sucesso!")
            atualizar_lista_produtos()  # Atualiza a exibição dos produtos.
            entry_nome_produto.delete(0, tk.END)  # Limpa o campo de entrada.
            entry_quantidade.delete(0, tk.END)  # Limpa o campo de entrada.
            entry_preco.delete(0, tk.END)  # Limpa o campo de entrada.
        except ValueError:  # Caso os valores não sejam numéricos.
            label_resultado_produto.config(text="Quantidade e preço devem ser numéricos.")

    # Função para remover um produto do estoque.
    def remover_produto():
        try:
            produto_id = int(entry_remover_produto.get())  # Obtém o ID do produto e o converte para inteiro.
            for i, produto in enumerate(produtos):  # Itera pela lista de produtos.
                if produto["id"] == produto_id:  # Verifica se o ID do produto corresponde.
                    del produtos[i]  # Remove o produto da lista.
                    label_resultado_produto.config(text="Produto removido com sucesso!")
                    atualizar_lista_produtos()  # Atualiza a exibição dos produtos.
                    entry_remover_produto.delete(0, tk.END)  # Limpa o campo de entrada.
                    return
            label_resultado_produto.config(text="Produto não encontrado.")  # Mensagem caso o produto não seja encontrado.
        except ValueError:  # Caso o valor do ID não seja numérico.
            label_resultado_produto.config(text="ID do produto deve ser numérico.")

    # Função para atualizar a lista de produtos exibida.
    def atualizar_lista_produtos():
        text_produtos.delete(1.0, tk.END)  # Limpa o widget de texto.
        for produto in produtos:  # Itera pela lista de produtos.
            # Adiciona as informações de cada produto ao widget de texto.
            text_produtos.insert(tk.END, f"ID: {produto['id']}, Nome: {produto['nome']}, Quantidade: {produto['quantidade']}, Preço: R$ {produto['preco']:.2f}\n")

    # Frame para adicionar produtos (cor verde).
    frame_adicionar = tk.Frame(estoque, bg="#008000")  # Cria um frame com fundo verde para adicionar produtos.
    frame_adicionar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Posiciona o frame na janela.

    # Widgets para adicionar produtos.
    label_nome_produto = ttk.Label(frame_adicionar, text="Nome do Produto:", background="#008000", foreground="white")  # Rótulo para o nome do produto.
    label_nome_produto.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_nome_produto = ttk.Entry(frame_adicionar)  # Campo de entrada para o nome do produto.
    entry_nome_produto.grid(row=0, column=1, padx=5, pady=5)

    label_quantidade = ttk.Label(frame_adicionar, text="Quantidade:", background="#008000", foreground="white")  # Rótulo para a quantidade.
    label_quantidade.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_quantidade = ttk.Entry(frame_adicionar)  # Campo de entrada para a quantidade.
    entry_quantidade.grid(row=1, column=1, padx=5, pady=5)

    label_preco = ttk.Label(frame_adicionar, text="Preço Unitário (R$):", background="#008000", foreground="white")  # Rótulo para o preço.
    label_preco.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_preco = ttk.Entry(frame_adicionar)  # Campo de entrada para o preço.
    entry_preco.grid(row=2, column=1, padx=5, pady=5)

    # Botão para adicionar produto.
    botao_adicionar_produto = ttk.Button(frame_adicionar, text="Adicionar Produto", command=adicionar_produto, style="my.TButton")
    botao_adicionar_produto.grid(row=3, columnspan=2, padx=5, pady=10)

    # Frame para remover produtos (cor vermelha).
    frame_remover = tk.Frame(estoque, bg="#FF0000")  # Cria um frame com fundo vermelho para remover produtos.
    frame_remover.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Widgets para remover produtos.
    label_remover_produto = ttk.Label(frame_remover, text="ID do Produto a Remover:", background="#FF0000", foreground="white")  # Rótulo para o ID do produto.
    label_remover_produto.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_remover_produto = ttk.Entry(frame_remover)  # Campo de entrada para o ID do produto.
    entry_remover_produto.grid(row=0, column=1, padx=5, pady=5)

    # Botão para remover produto.
    botao_remover_produto = ttk.Button(frame_remover, text="Remover Produto", command=remover_produto, style="my.TButton")
    botao_remover_produto.grid(row=1, columnspan=2, padx=5, pady=10)

    # Label para exibir mensagens de resultado sobre produtos.
    label_resultado_produto = ttk.Label(estoque, text="", background="#191970", foreground="white")  # Mensagens de feedback.
    label_resultado_produto.grid(row=2, column=0, padx=10, pady=5)

    # Text widget para listar os produtos.
    text_produtos = tk.Text(estoque, width=50, height=10, bg="lightgray")  # Área de texto para exibir os produtos.
    text_produtos.grid(row=3, column=0, padx=10, pady=10)
    # Função para adicionar um cliente à lista.
    def adicionar_cliente():
        nome = entry_nome_cliente.get()  # Obtém o nome do cliente do campo de entrada.
        cpf = entry_cpf_cliente.get()  # Obtém o CPF do cliente do campo de entrada.

        if not nome or not cpf:  # Verifica se os campos foram preenchidos.
            label_resultado_cliente.config(text="Por favor, preencha todos os campos do cliente.")
            return

        for cliente in clientes:  # Verifica se o CPF já está cadastrado.
            if cliente["cpf"] == cpf:
                label_resultado_cliente.config(text="CPF já cadastrado.")  # Mensagem de erro se o CPF já existe.
                return

        # Adiciona o cliente à lista de clientes.
        clientes.append({"nome": nome, "cpf": cpf})
        label_resultado_cliente.config(text="Cliente adicionado com sucesso!")  # Mensagem de sucesso.
        atualizar_lista_clientes()  # Atualiza a lista de clientes exibida.
        entry_nome_cliente.delete(0, tk.END)  # Limpa o campo de entrada do nome.
        entry_cpf_cliente.delete(0, tk.END)  # Limpa o campo de entrada do CPF.

    # Função para remover um cliente da lista.
    def remover_cliente():
        cpf = entry_remover_cpf_cliente.get()  # Obtém o CPF do cliente a ser removido.

        for i, cliente in enumerate(clientes):  # Itera pela lista de clientes.
            if cliente["cpf"] == cpf:  # Verifica se o CPF corresponde.
                del clientes[i]  # Remove o cliente da lista.
                label_resultado_cliente.config(text="Cliente removido com sucesso!")  # Mensagem de sucesso.
                atualizar_lista_clientes()  # Atualiza a lista de clientes exibida.
                entry_remover_cpf_cliente.delete(0, tk.END)  # Limpa o campo de entrada.
                return

        label_resultado_cliente.config(text="Cliente não encontrado.")  # Mensagem de erro se o cliente não for encontrado.

    # Função para atualizar a lista de clientes exibida.
    def atualizar_lista_clientes():
        text_clientes.delete(1.0, tk.END)  # Limpa o widget de texto.
        for cliente in clientes:  # Itera pela lista de clientes.
            # Adiciona as informações de cada cliente ao widget de texto.
            text_clientes.insert(tk.END, f"Nome: {cliente['nome']}, CPF: {cliente['cpf']}\n")

    # Função para abrir a janela de gerenciamento de clientes.
    def abrir_gerenciar_clientes():

        janela_clientes = tk.Toplevel(estoque)  # Cria uma nova janela como subjanela da janela principal.
        janela_clientes.title("Gerenciar Clientes")  # Define o título da janela.
        janela_clientes.configure(bg="#FFD700")  # Define a cor de fundo (amarelo).

        # Frame para adicionar cliente.
        frame_cadastro_cliente = tk.Frame(janela_clientes, bg="#FFD700")  # Cria um frame com fundo amarelo.
        frame_cadastro_cliente.pack(padx=10, pady=10)

        # Widgets para adicionar cliente.
        label_nome_cliente = ttk.Label(frame_cadastro_cliente, text="Nome do Cliente:", background="#FFD700")  # Rótulo para o nome do cliente.
        label_nome_cliente.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        global entry_nome_cliente  # Declara a variável global para uso em outras funções.
        entry_nome_cliente = ttk.Entry(frame_cadastro_cliente)  # Campo de entrada para o nome do cliente.
        entry_nome_cliente.grid(row=0, column=1, padx=5, pady=5)

        label_cpf_cliente = ttk.Label(frame_cadastro_cliente, text="CPF do Cliente:", background="#FFD700")  # Rótulo para o CPF.
        label_cpf_cliente.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        global entry_cpf_cliente  # Declara a variável global para uso em outras funções.
        entry_cpf_cliente = ttk.Entry(frame_cadastro_cliente)  # Campo de entrada para o CPF.
        entry_cpf_cliente.grid(row=1, column=1, padx=5, pady=5)

        # Botão para adicionar cliente.
        botao_adicionar_cliente = ttk.Button(frame_cadastro_cliente, text="Adicionar Cliente", command=adicionar_cliente)
        botao_adicionar_cliente.grid(row=2, columnspan=2, pady=10)

        # Frame para remover cliente.
        frame_remover_cliente = tk.Frame(janela_clientes, bg="#FF4500")  # Cria um frame com fundo vermelho.
        frame_remover_cliente.pack(padx=10, pady=10)

        # Widgets para remover cliente.
        label_remover_cpf_cliente = ttk.Label(frame_remover_cliente, text="CPF do Cliente a Remover:", background="#FF4500", foreground="white")  # Rótulo para o CPF do cliente.
        label_remover_cpf_cliente.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        global entry_remover_cpf_cliente  # Declara a variável global para uso em outras funções.
        entry_remover_cpf_cliente = ttk.Entry(frame_remover_cliente)  # Campo de entrada para o CPF do cliente.
        entry_remover_cpf_cliente.grid(row=0, column=1, padx=5, pady=5)

        # Botão para remover cliente.
        botao_remover_cliente = ttk.Button(frame_remover_cliente, text="Remover Cliente", command=remover_cliente)
        botao_remover_cliente.grid(row=1, columnspan=2, pady=10)

        # Label para exibir mensagens de resultado sobre clientes.
        global label_resultado_cliente  # Declara a variável global para uso em outras funções.
        label_resultado_cliente = ttk.Label(janela_clientes, text="", background="#FFD700")  # Mensagens de feedback.
        label_resultado_cliente.pack(pady=5)

        # Text widget para listar os clientes.
        global text_clientes  # Declara a variável global para uso em outras funções.
        text_clientes = tk.Text(janela_clientes, width=50, height=10, bg="lightgray")  # Área de texto para exibir os clientes.
        text_clientes.pack(padx=10, pady=10)

        atualizar_lista_clientes() # Atualiza a lista de clientes exibida na inicialização da janela.

    # Configurar colunas para distribuir corretamente o botão "Cliente"
    estoque.columnconfigure(0, weight=1)
    estoque.columnconfigure(1, weight=1)

    # Botão para abrir a janela de clientes
    botao_clientes = ttk.Button(estoque, text="Cliente", command=abrir_gerenciar_clientes)
    botao_clientes.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

    estoque.mainloop() # Inicia o loop principal do estoque


# Janela de Login e Cadastro

janela = tk.Tk() # Cria a janela principal da aplicação usando a biblioteca tkinter
janela.title("Tela de Login e Cadastro") # Define o título da janela como "Tela de Login e Cadastro".
janela.geometry("300x200") # Define as dimensões da janela para 300x200 pixels.

label_usuario = ttk.Label(janela, text="Usuário:") # Cria um rótulo (label) para identificar o campo de entrada do usuário.
label_usuario.pack(pady=5) # Posiciona o rótulo na janela com um espaçamento vertical (padding) de 5 pixels.
entry_usuario = ttk.Entry(janela) # Cria uma caixa de texto (entrada) para o usuário digitar seu nome de usuário.
entry_usuario.pack(pady=5) # Posiciona a caixa de texto na janela com um espaçamento vertical de 5 pixels.

label_senha = ttk.Label(janela, text="Senha:") # Cria um rótulo para identificar o campo de entrada de senha.
label_senha.pack(pady=5) # Posiciona o rótulo na janela com um espaçamento vertical de 5 pixels.
entry_senha = ttk.Entry(janela, show="*")  # Cria uma caixa de texto para entrada de senha, ocultando os caracteres digitados com "*".
entry_senha.pack(pady=5) # Posiciona a caixa de texto na janela com um espaçamento vertical de 5 pixels. 

botao_login = ttk.Button(janela, text="Login", command=realizar_login, style="my.TButton") # Cria um botão com o texto "Login". Ao ser clicado, chama a função `realizar_login`.
botao_login.config(style="green.TButton") # Aplica o estilo "green.TButton" ao botão, definindo sua aparência.
botao_login.pack(pady=5) # Posiciona o botão na janela com um espaçamento vertical de 5 pixels.

botao_cadastro = ttk.Button(janela, text="Cadastro", command=realizar_cadastro, style="my.TButton") # Cria um botão com o texto "Cadastro". Ao ser clicado, chama a função `realizar_cadastro`.
botao_cadastro.config(style="white.TButton") # Aplica o estilo "white.TButton" ao botão, definindo sua aparência.
botao_cadastro.pack(pady=5) # Posiciona o botão na janela com um espaçamento vertical de 5 pixels.

style = ttk.Style() # Cria um objeto de estilo para personalizar elementos da interface gráfica.


style.configure("green.TButton", background="green", foreground="white") # Define o estilo "green.TButton" com fundo verde e texto branco.


style.configure("white.TButton", background="white", foreground="black") # Define o estilo "white.TButton" com fundo branco e texto preto.


style.configure("my.TButton", padding=6) # Define o estilo "my.TButton" com um espaçamento interno (padding) de 6 pixels.


janela.mainloop() # Inicia o loop principal da janela